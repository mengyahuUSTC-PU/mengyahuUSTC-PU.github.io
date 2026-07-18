#!/usr/bin/env python3
"""Send a message to the private Discord channel via webhook.

Usage:
  discord_notify.py "message text"          # send arbitrary text
  discord_notify.py --topics [DATE]         # send today's deep-dive candidate list

Reads DISCORD_WEBHOOK_URL from the environment or from the .env file at the
repo root. Discord messages are capped at 2000 chars; long messages are split.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "automation" / "data"


def load_env():
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def send(text: str):
    url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not url:
        sys.exit("error: DISCORD_WEBHOOK_URL not set (env or .env)")
    # Split on paragraph boundaries to stay under the 2000-char limit.
    chunks, buf = [], ""
    for para in text.split("\n\n"):
        if len(buf) + len(para) + 2 > 1900:
            chunks.append(buf)
            buf = para
        else:
            buf = f"{buf}\n\n{para}" if buf else para
    chunks.append(buf)
    for chunk in chunks:
        resp = requests.post(url, json={"content": chunk}, timeout=20)
        resp.raise_for_status()


def topics_message(date: str) -> str:
    sel = json.loads((DATA / f"selection-{date}.json").read_text())
    cands = sel.get("deep_dive_candidates", [])
    if not cands:
        return f"📭 {date} 没有值得写深度的候选选题。"
    lines = [f"📋 **{date} 深度选题候选**（回复编号触发写稿，如 `1` 或 `1 3`；不回复则不写）", ""]
    for c in cands:
        lines.append(f"**{c['rank']}.** {c['title']}")
        lines.append(f"　💡 {c['why']}")
        lines.append(f"　🔗 {c['url']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    load_env()
    if len(sys.argv) > 1 and sys.argv[1] == "--topics":
        date = sys.argv[2] if len(sys.argv) > 2 else datetime.now(timezone.utc).strftime("%Y-%m-%d")
        send(topics_message(date))
        print(f"topic list for {date} sent")
    elif len(sys.argv) > 1:
        send(sys.argv[1])
        print("sent")
    else:
        sys.exit(__doc__)
