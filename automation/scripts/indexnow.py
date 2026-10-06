#!/usr/bin/env python3
"""Tell search engines when a page goes live.

The 2026-10 audit found Google leaving new articles undiscovered for weeks:
the best post since July was still "unknown to Google" a month after it went
live. Two free nudges:
- IndexNow, which Bing, Yandex, Seznam and Naver act on within minutes.
  Bing's index also feeds ChatGPT search and Copilot.
- Re-submitting the sitemap to Search Console, which prompts Google to read
  it again (Google does not take IndexNow).

poll_merged queues URLs the moment a PR merges. The hourly flush pings only
the URLs that already answer 200, because GitHub Pages takes a couple of
minutes to deploy and a crawler should never be sent to a 404. Nothing is
pinged until the key file itself is live.

    indexnow.py queue URL...   add URLs (poll_merged does this)
    indexnow.py flush          ping everything queued that is now live
"""

import fcntl
import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
QUEUE = REPO_ROOT / "automation" / "data" / "indexnow-queue.json"
HOST = "mengyahu.com"
# Public by design: IndexNow proves site ownership by fetching /<key>.txt.
KEY = "977d4f1e9e8255d9189de4022a21c64d"
KEY_URL = f"https://{HOST}/{KEY}.txt"
SITEMAP = f"https://{HOST}/sitemap-index.xml"
GIVE_UP = timedelta(days=3)  # a URL that never went live is dropped, with a notice


@contextmanager
def locked():
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with QUEUE.with_suffix(".lock").open("w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _load() -> dict:
    try:
        return json.loads(QUEUE.read_text())
    except Exception:
        return {}


def _save(queue: dict):
    tmp = QUEUE.with_name(QUEUE.name + ".tmp")
    tmp.write_text(json.dumps(queue, indent=1))
    tmp.replace(QUEUE)


def queue_urls(urls):
    now = datetime.now(timezone.utc).isoformat()
    with locked():
        queue = _load()
        for url in urls:
            queue.setdefault(url, now)
        _save(queue)


def _live(url: str) -> bool:
    try:
        return requests.get(url, timeout=20, allow_redirects=False).status_code == 200
    except requests.RequestException:
        return False


def _resubmit_sitemap() -> str:
    try:
        from google.auth.transport.requests import Request
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_file(
            os.environ["GA_SA_KEY"], scopes=["https://www.googleapis.com/auth/webmasters"])
        creds.refresh(Request())
        site = requests.utils.quote(f"sc-domain:{HOST}", safe="")
        r = requests.put(
            f"https://www.googleapis.com/webmasters/v3/sites/{site}/sitemaps/"
            f"{requests.utils.quote(SITEMAP, safe='')}",
            headers={"Authorization": f"Bearer {creds.token}"}, timeout=60)
        return "google sitemap resubmitted" if r.ok else f"google sitemap {r.status_code}"
    except Exception as exc:  # noqa: BLE001 — Bing's ping must not depend on Google's
        return f"google sitemap failed: {str(exc)[:120]}"


def flush() -> str:
    with locked():
        queue = _load()
        if not queue:
            return ""
        if not _live(KEY_URL):
            return f"key file not live yet ({KEY_URL}); {len(queue)} URL(s) waiting"
        now = datetime.now(timezone.utc)
        live = [u for u in queue if _live(u)]
        stale = [u for u in queue if u not in live
                 and now - datetime.fromisoformat(queue[u]) > GIVE_UP]
        notes = []
        if live:
            r = requests.post("https://api.indexnow.org/indexnow", timeout=60, json={
                "host": HOST, "key": KEY, "keyLocation": KEY_URL, "urlList": live})
            if r.status_code in (200, 202):
                notes.append(f"indexnow {r.status_code}: {len(live)} URL(s)")
                for u in live:
                    queue.pop(u, None)
                notes.append(_resubmit_sitemap())
            else:
                notes.append(f"indexnow FAILED {r.status_code}: {r.text[:160]}")
        for u in stale:
            queue.pop(u, None)
        _save(queue)
    if stale:
        try:
            from discord_notify import send
            send("⚠️ 这些网址三天了还打不开，已停止通知搜索引擎：\n" + "\n".join(stale[:10]))
        except Exception:
            pass
    return " · ".join(notes)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    from discord_notify import load_env
    load_env()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "flush"
    if cmd == "queue":
        queue_urls(sys.argv[2:])
    else:
        result = flush()
        if result:
            print(f"[{datetime.now(timezone.utc):%Y-%m-%d %H:%MZ}] {result}")
