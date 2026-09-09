#!/usr/bin/env python3
"""Turn a draft article into a podcast episode on a private feed.

The bottleneck in this pipeline is reading time: PRs pile up unread. Reading is
slower than listening for this user, and the gym is dead time, so every deep
dive gets an audio version the moment its PR opens, delivered through a normal
podcast app (offline download, lock screen controls, resume where you left off).

Usage: podcast.py <markdown-path> [--pr <number>] [--url <pr url>]
"""

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path
import time
from datetime import datetime, timezone
from email.utils import format_datetime
import numpy as np
import soundfile as sf

# Text preparation and phonemization live with the pipeline; only the model
# weights stay outside the repo.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tts"))
import prep      # noqa: E402  markdown -> text meant to be heard
import speech    # noqa: E402  text -> Kokoro phonemes, Chinese with English in it

PODCAST_DIR = Path("/home/mia/podcast")
EPISODE_DIR = PODCAST_DIR / "episodes"
STATE_FILE = PODCAST_DIR / "episodes.json"
MODEL = "/home/mia/tts/kokoro-v1.0.onnx"
VOICES = "/home/mia/tts/voices-v1.0.bin"
VOICE = "zf_xiaoxiao"
RATE = 24000
KEEP = 60  # episodes retained; a phone only ever needs the recent ones

FEED_TITLE = "Mengya 的草稿朗读"
FEED_DESC = ("每篇深度文章在 PR 开出来的时候自动转成音频，方便在健身房和路上听审。"
             "内容是尚未发布的草稿，仅本人使用。")


def base_url() -> str:
    token = (PODCAST_DIR / "token").read_text().strip()
    return f"https://api.mengyahu.com/podcast/{token}"


def frontmatter(markdown: str) -> dict:
    if not markdown.startswith("---"):
        return {}
    head = markdown.split("---", 2)[1]
    out = {}
    for line in head.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def synthesize(text: str, out_wav: Path) -> float:
    """Speak the article. Returns audio length in seconds."""
    from kokoro_onnx import Kokoro

    kokoro = Kokoro(MODEL, VOICES)
    pieces = prep.chunks(text)
    gap = np.zeros(int(RATE * 0.25), dtype=np.float32)
    para_gap = np.zeros(int(RATE * 0.6), dtype=np.float32)

    segments = []
    for piece in pieces:
        phonemes = speech.mixed_phonemes(piece)
        if not phonemes.strip():
            continue
        samples, _ = kokoro.create(phonemes, voice=VOICE, speed=1.0, is_phonemes=True)
        segments.append(samples)
        segments.append(para_gap if piece.endswith(("。", "！", "？")) else gap)

    audio = np.concatenate(segments) if segments else np.zeros(1, dtype=np.float32)
    sf.write(out_wav, audio, RATE)
    return len(audio) / RATE


def encode(wav: Path, mp3: Path, title: str):
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
         "-codec:a", "libmp3lame", "-b:a", "64k", "-ac", "1",
         "-metadata", f"title={title}", "-metadata", "artist=Mengya (Mia) Hu",
         "-metadata", f"album={FEED_TITLE}", str(mp3)],
        check=True,
    )
    wav.unlink(missing_ok=True)


def load_state() -> list:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return []


def write_feed(episodes: list):
    """A plain RSS 2.0 feed with the iTunes tags podcast apps expect."""
    root = base_url()
    items = []
    for ep in episodes[:KEEP]:
        link = ep.get("pr_url") or "https://mengyahu.com"
        items.append(f"""    <item>
      <title>{html.escape(ep['title'])}</title>
      <description>{html.escape(ep.get('summary', ''))}</description>
      <link>{html.escape(link)}</link>
      <guid isPermaLink="false">{ep['slug']}</guid>
      <pubDate>{ep['pub_date']}</pubDate>
      <enclosure url="{root}/episodes/{ep['file']}" length="{ep['bytes']}" type="audio/mpeg"/>
      <itunes:duration>{int(ep['seconds'])}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
    </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{html.escape(FEED_TITLE)}</title>
    <link>https://mengyahu.com</link>
    <language>zh-CN</language>
    <description>{html.escape(FEED_DESC)}</description>
    <itunes:author>Mengya (Mia) Hu</itunes:author>
    <itunes:explicit>false</itunes:explicit>
    <itunes:block>Yes</itunes:block>
{chr(10).join(items)}
  </channel>
</rss>
"""
    (PODCAST_DIR / "feed.xml").write_text(feed)


def prune(episodes: list):
    keep = {ep["file"] for ep in episodes[:KEEP]}
    for old in EPISODE_DIR.glob("*.mp3"):
        if old.name not in keep:
            old.unlink()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown")
    ap.add_argument("--pr", default="")
    ap.add_argument("--url", default="")
    ap.add_argument("--quiet", action="store_true", help="skip the Discord notice")
    args = ap.parse_args()

    path = Path(args.markdown)
    markdown = path.read_text()
    meta = frontmatter(markdown)
    slug = meta.get("slug") or path.stem
    if slug.startswith("briefing-"):
        print("briefings are not read aloud; skipping")
        return

    title = meta.get("title", slug)
    EPISODE_DIR.mkdir(parents=True, exist_ok=True)

    started = time.time()
    text = prep.speech_text(markdown)
    wav = EPISODE_DIR / f"{slug}.wav"
    seconds = synthesize(text, wav)
    mp3 = EPISODE_DIR / f"{slug}.mp3"
    encode(wav, mp3, title)

    episodes = [ep for ep in load_state() if ep["slug"] != slug]
    episodes.insert(0, {
        "slug": slug,
        "title": (f"PR #{args.pr}｜{title}" if args.pr else title),
        "summary": meta.get("description", ""),
        "file": mp3.name,
        "bytes": mp3.stat().st_size,
        "seconds": seconds,
        "pub_date": format_datetime(datetime.now(timezone.utc)),
        "pr_url": args.url,
    })
    STATE_FILE.write_text(json.dumps(episodes, ensure_ascii=False, indent=2))
    write_feed(episodes)
    prune(episodes)

    minutes = seconds / 60
    print(f"{slug}: {minutes:.1f} min audio, synthesized in {(time.time()-started)/60:.1f} min")

    if not args.quiet:
        sys.path.insert(0, "/home/mia/site/automation/scripts")
        from discord_notify import send
        where = f"（PR #{args.pr}）" if args.pr else ""
        send(f"🎧 **朗读版已就绪**{where}：{title}\n"
             f"约 {minutes:.0f} 分钟 · 打开播客 App 刷新一下就能听")


if __name__ == "__main__":
    main()
