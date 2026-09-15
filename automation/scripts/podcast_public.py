#!/usr/bin/env python3
"""Publish an episode of 《胡说 AI》 — the public podcast.

Two feeds exist and they must never be confused. The private one carries
DRAFT audio for the owner's own review; this one carries the FINAL published
text, read after fact-checking and her edits, and it is meant to be found:
Apple, Spotify and 小宇宙 subscribe to it, and mengyahu.com plays it under
each article.

    podcast_public.py <slug>            publish (or re-publish) one article
    podcast_public.py --list            what is in the public feed

Audio is synthesized through the second Azure Speech resource, whose free
monthly quota is separate from the draft reader's.
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent                 # /home/mia/site
sys.path.insert(0, str(HERE.parent / "tts"))
sys.path.insert(0, str(HERE))

PUBLIC = Path("/home/mia/podcast-public")
EPISODES = PUBLIC / "episodes"
STATE = PUBLIC / "episodes.json"
MANIFEST = REPO / "src" / "data" / "podcast.json"   # the site reads this
SITE = "https://mengyahu.com"
HOST = "https://podcast.mengyahu.com"
GIT_LOCK = "/tmp/pipeline-git.lock"

SHOW = {
    "title": "胡说 AI",
    "author": "胡梦雅",
    "email": "mia@mengyahu.com",
    "link": f"{SITE}/zh/podcast/",
    "language": "zh-cn",
    "category": "Technology",
    "description": (
        "我是胡梦雅，在微软 Responsible AI 团队做应用科学家。这里是我博客深度文章的音频版："
        "AI 安全、行业趋势、工程实践，还有我正好奇的前沿科技。"
        "名字有两层意思：胡说 AI，也是那个一本正经胡说八道的 AI。"
        "音频由 AI 语音朗读，观点仅代表个人。"
    ),
}


def frontmatter(markdown: str) -> dict:
    if not markdown.startswith("---"):
        return {}
    out = {}
    for line in markdown.split("---", 2)[1].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def load(path: Path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def write_atomic(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)


def synthesize(text: str, out: Path) -> float:
    """Use the public resource, and keep its usage counter separate."""
    os.environ["AZURE_SPEECH_KEY"] = os.environ["AZURE_SPEECH_KEY_PUBLIC"]
    os.environ["AZURE_SPEECH_REGION"] = os.environ.get("AZURE_SPEECH_REGION_PUBLIC", "eastus")
    import azure_tts
    azure_tts.USAGE_DIR = Path("/home/mia/podcast-public/usage")
    return azure_tts.synthesize(text, out)


def build_feed(episodes: list) -> str:
    items = []
    for ep in episodes:
        items.append(f"""    <item>
      <title>{html.escape(ep['title'])}</title>
      <link>{html.escape(ep['article'])}</link>
      <description><![CDATA[{ep['description']}]]></description>
      <itunes:summary><![CDATA[{ep['description']}]]></itunes:summary>
      <guid isPermaLink="false">{ep['slug']}@{ep['version']}</guid>
      <pubDate>{ep['pub_date']}</pubDate>
      <enclosure url="{HOST}/episodes/{ep['file']}" length="{ep['bytes']}" type="audio/mpeg"/>
      <itunes:duration>{int(ep['seconds'])}</itunes:duration>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
    </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{html.escape(SHOW['title'])}</title>
    <link>{SHOW['link']}</link>
    <language>{SHOW['language']}</language>
    <copyright>© {datetime.now(timezone.utc).year} {html.escape(SHOW['author'])}</copyright>
    <description><![CDATA[{SHOW['description']}]]></description>
    <atom:link href="{HOST}/feed.xml" rel="self" type="application/rss+xml"/>
    <itunes:author>{html.escape(SHOW['author'])}</itunes:author>
    <itunes:summary><![CDATA[{SHOW['description']}]]></itunes:summary>
    <itunes:type>episodic</itunes:type>
    <itunes:explicit>false</itunes:explicit>
    <itunes:image href="{HOST}/cover.jpg"/>
    <itunes:category text="{SHOW['category']}"/>
    <itunes:owner>
      <itunes:name>{html.escape(SHOW['author'])}</itunes:name>
      <itunes:email>{SHOW['email']}</itunes:email>
    </itunes:owner>
{chr(10).join(items)}
  </channel>
</rss>
"""


def update_site_manifest(episodes: list):
    """One small file the site reads to show a player under the article."""
    manifest = {ep["slug"]: {"url": f"{HOST}/episodes/{ep['file']}",
                             "seconds": int(ep["seconds"]),
                             "published": ep["pub_date"]}
                for ep in episodes}
    write_atomic(MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    rel = MANIFEST.relative_to(REPO)
    subprocess.run(["flock", GIT_LOCK, "bash", "-c", f"""
        cd {REPO} &&
        git add {rel} &&
        git diff --cached --quiet || (
          git -c user.name=brand-automation -c user.email={SHOW['email']} \
            commit -q -m 'Publish podcast audio for the latest article

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>' &&
          git pull -q --rebase && git push -q origin master
        )"""], check=False)


def publish(slug: str, quiet: bool = False) -> dict:
    import prep
    md_path = REPO / "src" / "content" / "blog" / "zh" / f"{slug}.md"
    if not md_path.exists():
        raise SystemExit(f"{slug}: no published Chinese article (audio is made from the final text)")
    markdown = md_path.read_text()
    meta = frontmatter(markdown)
    title = meta.get("title", slug)
    article = f"{SITE}/zh/{slug}/"

    started = time.time()
    EPISODES.mkdir(parents=True, exist_ok=True)
    mp3 = EPISODES / f"{slug}.mp3"
    seconds = synthesize(prep.speech_text(markdown), mp3)

    episodes = [e for e in load(STATE, []) if e["slug"] != slug]
    episodes.insert(0, {
        "slug": slug,
        "title": title,
        "description": meta.get("description", ""),
        "article": article,
        "file": mp3.name,
        "bytes": mp3.stat().st_size,
        "seconds": seconds,
        "version": int(time.time()),
        "pub_date": format_datetime(datetime.now(timezone.utc)),
    })
    episodes.sort(key=lambda e: e["version"], reverse=True)
    write_atomic(STATE, json.dumps(episodes, ensure_ascii=False, indent=2))
    write_atomic(PUBLIC / "feed.xml", build_feed(episodes))
    update_site_manifest(episodes)

    result = {"slug": slug, "minutes": seconds / 60, "took": time.time() - started,
              "episodes": len(episodes)}
    print(f"{slug}: {result['minutes']:.1f} min, {result['took']:.0f}s, feed now has {len(episodes)} episode(s)")
    if not quiet:
        from discord_notify import send
        send(f"🎙️ **《胡说 AI》已更新**：{title}\n"
             f"约 {result['minutes']:.0f} 分钟 · {article}")
    return result


def load_env(path=Path("/home/mia/site/.env")):
    for line in path.read_text().splitlines() if path.exists() else []:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


if __name__ == "__main__":
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    if args.list:
        for e in load(STATE, []):
            print(f"{e['pub_date'][:16]}  {int(e['seconds'])//60:>3}分  {e['slug']}  {e['title'][:40]}")
    elif args.slug:
        publish(args.slug, quiet=args.quiet)
    else:
        ap.error("give a slug or --list")
