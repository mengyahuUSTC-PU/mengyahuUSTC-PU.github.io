#!/usr/bin/env python3
"""Watch for the show appearing in podcast directories.

Apple takes a few days to review a new show. Rather than have the owner keep
checking, this runs daily: the moment Apple's catalogue returns our feed, the
listen link is written into the site and announced in Discord.

    check_directories.py          check and, if something changed, publish it
    check_directories.py --show   print what is currently known
"""

import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
LINKS = REPO / "src" / "data" / "podcast-links.json"
FEED = "https://podcast.mengyahu.com/feed.xml"
SHOW_NAME = "胡说 AI"
GIT_LOCK = "/tmp/pipeline-git.lock"


def apple_link() -> str | None:
    """Apple's public catalogue search. A match on our feed URL is proof the
    show is live; a name match alone could be somebody else's show."""
    for country in ("us", "cn"):
        url = ("https://itunes.apple.com/search?" + urllib.parse.urlencode(
            {"term": SHOW_NAME, "entity": "podcast", "country": country, "limit": 25}))
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                data = json.load(r)
        except Exception:
            continue
        for item in data.get("results", []):
            if (item.get("feedUrl") or "").rstrip("/") == FEED.rstrip("/"):
                return item.get("collectionViewUrl") or item.get("trackViewUrl")
    return None


def load() -> dict:
    try:
        return json.loads(LINKS.read_text())
    except Exception:
        return {}


def publish(links: dict):
    LINKS.parent.mkdir(parents=True, exist_ok=True)
    tmp = LINKS.with_suffix(".tmp")
    tmp.write_text(json.dumps(links, ensure_ascii=False, indent=2, sort_keys=True))
    tmp.replace(LINKS)
    rel = LINKS.relative_to(REPO)
    subprocess.run(["flock", GIT_LOCK, "bash", "-c", f"""
        cd {REPO} && git add {rel} && (git diff --cached --quiet || (
          git -c user.name=brand-automation -c user.email=humengyahumy@gmail.com \
            commit -q -m 'Add a directory listing link for the podcast

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>' &&
          git pull -q --rebase && git push -q origin master))"""], check=False)


def notify(text: str):
    try:
        sys.path.insert(0, str(HERE))
        from discord_notify import send
        send(text)
    except Exception:
        pass


def main():
    links = load()
    if "--show" in sys.argv:
        print(json.dumps(links, ensure_ascii=False, indent=2) if links else "(还没有任何平台链接)")
        return
    found = apple_link()
    if found and links.get("apple") != found:
        links["apple"] = found
        publish(links)
        notify(f"🎉 **《胡说 AI》已经在 Apple Podcasts 上线了**\n{found}\n"
               f"网站的播客页已经自动加上收听链接。")
        print("apple:", found)
    else:
        print("apple:", "already recorded" if found else "not in the catalogue yet")


if __name__ == "__main__":
    main()
