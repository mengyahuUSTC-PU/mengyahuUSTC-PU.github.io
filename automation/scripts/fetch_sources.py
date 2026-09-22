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


def fetch_hf_papers():
    """HuggingFace daily papers — community-curated research feed.

    Research items for the briefing's 研究速递 section (user request
    2026-08-12: LLM/FM, RL, AI4Science, AI4Finance, conference news).
    Same-day papers haven't accumulated votes yet, so pull a multi-day
    window and let upvotes (a decent quality proxy) rank it."""
    resp = requests.get(
        "https://huggingface.co/api/daily_papers?limit=60",
        timeout=30, headers={"User-Agent": "Mozilla/5.0 (brand-pipeline)"})
    resp.raise_for_status()
    items = []
    for it in resp.json():
        paper = it.get("paper") or {}
        aid = paper.get("id")
        if not aid:
            continue
        upvotes = int(paper.get("upvotes") or 0)
        items.append({
            "source": "hf-daily-papers",
            "title": (paper.get("title") or "").strip().replace("\n", " "),
            "url": f"https://arxiv.org/abs/{aid}",
            "summary": f"[HF 社区 {upvotes} 赞] " + clean(paper.get("summary") or ""),
            "published": (it.get("publishedAt") or "")[:10],
            "_upvotes": upvotes,
        })
    items.sort(key=lambda x: -x["_upvotes"])
    for it in items:
        it.pop("_upvotes", None)
    return items[:12]


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
                "score": s.get("score", 0),
                "published": datetime.fromtimestamp(
                    s.get("time", 0), tz=timezone.utc
                ).isoformat(),
            }
        )
        time.sleep(0.1)
    return items


def _radar_key(title: str) -> str:
    """Title without the trailing " - Publisher", lowercased: syndicated copies
    of one wire story collapse to a single key."""
    import re as _re
    base = _re.sub(r"\s+-\s+[^-]{2,40}$", "", title or "").lower()
    return _re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", base)[:80]


def fetch_launch_radar():
    """Google News queries that catch launches from labs we do not follow."""
    from config import LAUNCH_RADAR

    items, failed, seen = [], [], set()
    for name, query in LAUNCH_RADAR:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        try:
            parsed = feedparser.parse(requests.get(url, headers=UA, timeout=25).content)
            for e in parsed.entries[:12]:
                when = entry_datetime(e)
                if when and when < CUTOFF:
                    continue
                if not matches(e.get("title", ""), HN_KEYWORDS):
                    continue
                key = _radar_key(e.get("title", ""))
                if not key or key in seen:
                    continue
                seen.add(key)
                items.append({
                    "source": name,
                    "title": clean(e.get("title", ""), 200),
                    "url": e.get("link", ""),
                    "summary": clean(e.get("summary", ""), 300),
                    "published": (when or NOW).isoformat(),
                })
        except Exception as exc:
            failed.append({"source": name, "error": str(exc)[:200]})
    return items[:18], failed


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


def add_heat(items):
    """Tag each item with how many DISTINCT sources mention its distinctive
    names, over this pool and the two before it.

    Counting raw mentions rewarded whoever repeats themselves most — one wire
    story syndicated ten times, or a site advertising its own conference.
    Distinct sources is the thing that actually means "everyone is talking
    about this".
    """
    import re as _re
    from collections import Counter, defaultdict

    # Words that are capitalised but carry no story: sentence starters, the
    # publishers themselves, and the conference circuit.
    STOP = {
        "The", "This", "That", "With", "From", "What", "How", "Why", "New", "And",
        "For", "Its", "Has", "Now", "You", "Your", "Are", "Not", "All", "Can",
        "Here", "After", "Before", "More", "Most", "Best", "First", "Last",
        "AI", "LLM", "GPT", "API", "US", "UK", "EU", "CEO", "IT", "PDF",
        "TechCrunch", "VentureBeat", "Reuters", "Bloomberg", "Verge", "Wired",
        "Disrupt", "Register", "Post", "Times", "Journal", "News", "Blog",
        "Hacker", "Show", "Ask", "Announcing", "Introducing",
        # The radar queries contain these verbs, so every radar headline
        # carries them; they mark the shape of the news, never the subject.
        "Launch", "Launches", "Launched", "Launching", "Announce", "Announces",
        "Announced", "Unveils", "Unveiled", "Debuts", "Release", "Releases",
        "Released", "Introduces", "Rolls", "Adds", "Brings", "Hits", "Says",
    }

    # Vendor names appear in half the pool on any given day, so they say
    # nothing about whether one story is breaking. Heat should come from the
    # specific thing being talked about: Muse, Jev, Astra — not "Google".
    VENDORS = {
        "Google", "Meta", "OpenAI", "Anthropic", "Microsoft", "Amazon", "Apple",
        "Nvidia", "DeepMind", "ChatGPT", "Claude", "Gemini", "Llama", "Copilot",
        "China", "Silicon", "Valley",
    }

    def names_raw(text):
        return {w for w in _re.findall(r"\b[A-Z][A-Za-z0-9.\-]{2,}\b", text or "")
                if w not in STOP and w not in VENDORS}

    def names(text):
        cap = max(6, archive_total * GENERIC_SHARE)
        return {w for w in names_raw(text) if doc_freq.get(w, 0) <= cap}

    def read_pool(path):
        try:
            prev = json.loads(path.read_text())
            return prev if isinstance(prev, list) else prev.get("items", [])
        except Exception:
            return []

    pools = sorted(DATA_DIR.glob("pool-*.json"))
    history = [it for p in pools[-3:-1] for it in read_pool(p)]

    # Generic-word filter, measured against our own archive. Words like Models,
    # Alignment or Reasoning turn up in 3-6% of everything we fetch; a name
    # that marks an actual event sits near or below 1% (Muse 0.7%, Codex 0.4%,
    # Jev 0.06%). Counting DAYS instead of items was the first attempt and it
    # was wrong: a story running for two weeks looked "common" exactly when it
    # was hottest, which is how Muse got dropped.
    doc_freq = Counter()
    archive_total = 0
    for path in pools[-30:]:
        rows = read_pool(path)
        archive_total += len(rows)
        for it in rows:
            for w in names_raw(it.get("title", "")):
                doc_freq[w] += 1
    GENERIC_SHARE = 0.015          # ~1.5% of the archive

    def bucket(item: dict) -> str:
        """One voice per outlet. Radar items all share a source name, so use
        the publisher Google News appends to the title — identical wire copies
        were already collapsed when the radar was fetched."""
        source = str(item.get("source", ""))
        if not source.startswith("发布雷达"):
            return source
        tail = _re.search(r"\s+-\s+([^-]{2,40})$", item.get("title", "") or "")
        return f"radar:{tail.group(1).strip().lower()}" if tail else "radar:unknown"

    sources_by_name = defaultdict(set)
    for it in items + history:
        b = bucket(it)
        for n in names(it.get("title", "")):
            sources_by_name[n].add(b)

    for it in items:
        ns = names(it.get("title", ""))
        it["heat"] = max((len(sources_by_name[n]) for n in ns), default=0)
        hot = [n for n in ns if len(sources_by_name[n]) >= 3]
        if hot:
            it["hot_names"] = sorted(hot, key=lambda n: -len(sources_by_name[n]))[:3]
        else:
            it.pop("hot_names", None)
    return items


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    pool = {"fetched_at": NOW.isoformat(), "items": [], "failed_sources": []}

    for fn in (fetch_arxiv, fetch_hackernews, fetch_hf_papers):
        try:
            pool["items"].extend(fn())
        except Exception as exc:
            pool["failed_sources"].append({"source": fn.__name__, "error": str(exc)[:200]})

    for fetcher in (fetch_rss, fetch_scraped, fetch_launch_radar):
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
    pool["items"] = add_heat(unique)

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
