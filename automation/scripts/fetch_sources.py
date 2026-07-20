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
    SCRAPE_SOURCES,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
from zoneinfo import ZoneInfo
PT_DATE = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
# Full browser UA: Substack and others 403 on obvious bot agents.
UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}
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
    for entry in RSS_FEEDS:
        name, url = entry[0], entry[1]
        keyword_gate = len(entry) > 2 and entry[2] == "filter"
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
            if keyword_gate and not matches(
                f"{e.get('title', '')} {e.get('summary', '')}", HN_KEYWORDS
            ):
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


def fetch_scraped():
    """Page-scrape fallback for sources with no working feed (no dates available)."""
    items, failed = [], []
    for name, page_url, href_re, prefix in SCRAPE_SOURCES:
        try:
            resp = requests.get(page_url, headers=UA, timeout=25)
            resp.raise_for_status()
            hrefs = list(dict.fromkeys(re.findall(href_re, resp.text)))[:10]
            if not hrefs:
                raise ValueError("no links matched")
        except Exception as exc:
            failed.append({"source": name, "url": page_url, "error": str(exc)[:200]})
            continue
        for href in hrefs:
            items.append(
                {
                    "source": name,
                    "title": clean(href.rstrip("/").split("/")[-1].replace("-", " "), 200),
                    "url": prefix + href,
                    "summary": "(scraped link; open for details)",
                    "published": "",
                }
            )
    return items, failed


def historical_urls():
    """URLs seen in earlier pool files — used to drop repeats from undated scrapes."""
    seen = set()
    for f in sorted(DATA_DIR.glob("pool-*.json"))[-14:]:
        if f.name == f"pool-{PT_DATE}.json":
            continue
        try:
            for item in json.loads(f.read_text()).get("items", []):
                seen.add(item.get("url", ""))
        except Exception:
            continue
    return seen


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    pool = {"fetched_at": NOW.isoformat(), "items": [], "failed_sources": []}

    for fn in (fetch_arxiv, fetch_hackernews):
        try:
            pool["items"].extend(fn())
        except Exception as exc:
            pool["failed_sources"].append({"source": fn.__name__, "error": str(exc)[:200]})

    for fetcher in (fetch_rss, fetch_scraped):
        got, failed = fetcher()
        pool["items"].extend(got)
        pool["failed_sources"].extend(failed)

    # De-duplicate by URL, within today's pool and against recent history.
    seen, unique = historical_urls(), []
    for item in pool["items"]:
        if item["url"] in seen:
            continue
        seen.add(item["url"])
        unique.append(item)
    pool["items"] = unique

    out = DATA_DIR / f"pool-{PT_DATE}.json"
    out.write_text(json.dumps(pool, ensure_ascii=False, indent=2))
    print(
        f"{out.name}: {len(pool['items'])} items, "
        f"{len(pool['failed_sources'])} failed sources"
    )
    for f in pool["failed_sources"]:
        print(f"  [skip] {f['source']}: {f['error'][:80]}")


if __name__ == "__main__":
    main()
