#!/usr/bin/env python3
"""Daily source fetcher.

Pulls arXiv, Hacker News, and a list of RSS/Atom feeds, filters for
relevance, and writes the day's raw item pool to
automation/data/pool-YYYY-MM-DD.json.

Failing sources are recorded in the output under "failed_sources" and
never abort the run.
"""

import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    ARXIV_CATEGORIES,
    ARXIV_MAX_RESULTS,
    HN_KEYWORDS,
    HN_TOP_LIMIT,
    MAX_AGE_DAYS,
    RSS_FEEDS,
    SAFETY_KEYWORDS,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
UA = {"User-Agent": "Mozilla/5.0 (brand-automation fetcher; personal blog pipeline)"}
NOW = datetime.now(timezone.utc)
CUTOFF = NOW - timedelta(days=MAX_AGE_DAYS)


def matches(text: str, keywords) -> bool:
    text = text.lower()
    return any(k in text for k in keywords)


def clean(text: str, limit: int = 400) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def fetch_arxiv():
    cat_query = "+OR+".join(f"cat:{c}" for c in ARXIV_CATEGORIES)
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query={cat_query}&sortBy=submittedDate&sortOrder=descending"
        f"&max_results={ARXIV_MAX_RESULTS}"
    )
    feed = feedparser.parse(url)
    items = []
    for e in feed.entries:
        text = f"{e.get('title', '')} {e.get('summary', '')}"
        if not matches(text, SAFETY_KEYWORDS):
            continue
        items.append(
            {
                "source": "arXiv",
                "title": clean(e.get("title", ""), 200),
                "url": e.get("link", ""),
                "summary": clean(e.get("summary", "")),
                "published": e.get("published", ""),
            }
        )
    return items


def fetch_hackernews():
    top = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json", headers=UA, timeout=20
    ).json()[:HN_TOP_LIMIT]
    items = []
    for story_id in top:
        try:
            s = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                headers=UA,
                timeout=20,
            ).json()
        except Exception:
            continue
        if not s or s.get("type") != "story":
            continue
        title = s.get("title", "")
        if not matches(title, HN_KEYWORDS):
            continue
        items.append(
            {
                "source": "Hacker News",
                "title": clean(title, 200),
                "url": s.get("url") or f"https://news.ycombinator.com/item?id={story_id}",
                "summary": f"{s.get('score', 0)} points, {s.get('descendants', 0)} comments",
                "published": datetime.fromtimestamp(
                    s.get("time", 0), tz=timezone.utc
                ).isoformat(),
            }
        )
        time.sleep(0.1)
    return items


def entry_datetime(e):
    for key in ("published_parsed", "updated_parsed"):
        t = e.get(key)
        if t:
            return datetime(*t[:6], tzinfo=timezone.utc)
    return None


def fetch_rss():
    items, failed = [], []
    for name, url in RSS_FEEDS:
        try:
            resp = requests.get(url, headers=UA, timeout=25)
            feed = feedparser.parse(resp.content)
            if not feed.entries:
                raise ValueError(f"no entries (HTTP {resp.status_code})")
        except Exception as exc:
            failed.append({"source": name, "url": url, "error": str(exc)[:200]})
            continue
        for e in feed.entries[:15]:
            dt = entry_datetime(e)
            if dt and dt < CUTOFF:
                continue
            items.append(
                {
                    "source": name,
                    "title": clean(e.get("title", ""), 200),
                    "url": e.get("link", ""),
                    "summary": clean(e.get("summary", e.get("description", ""))),
                    "published": dt.isoformat() if dt else "",
                }
            )
    return items, failed


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    pool = {"fetched_at": NOW.isoformat(), "items": [], "failed_sources": []}

    for fn in (fetch_arxiv, fetch_hackernews):
        try:
            pool["items"].extend(fn())
        except Exception as exc:
            pool["failed_sources"].append({"source": fn.__name__, "error": str(exc)[:200]})

    rss_items, rss_failed = fetch_rss()
    pool["items"].extend(rss_items)
    pool["failed_sources"].extend(rss_failed)

    # De-duplicate by URL.
    seen, unique = set(), []
    for item in pool["items"]:
        if item["url"] in seen:
            continue
        seen.add(item["url"])
        unique.append(item)
    pool["items"] = unique

    out = DATA_DIR / f"pool-{NOW.strftime('%Y-%m-%d')}.json"
    out.write_text(json.dumps(pool, ensure_ascii=False, indent=2))
    print(
        f"{out.name}: {len(pool['items'])} items, "
        f"{len(pool['failed_sources'])} failed sources"
    )
    for f in pool["failed_sources"]:
        print(f"  [skip] {f['source']}: {f['error'][:80]}")


if __name__ == "__main__":
    main()
