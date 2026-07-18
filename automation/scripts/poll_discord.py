#!/usr/bin/env python3
"""Poll the Discord channel for the user's topic-selection replies.

Runs from cron every few minutes. When the user replies with numbers
(e.g. "1" or "1 3") after a topic list was posted, triggers deep-dive
generation + PR creation for each selected rank, then posts the PR links
back to the channel.

State (last processed message id) lives in automation/data/state/discord.json.
Env: DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID (env or .env at repo root).
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "automation" / "data"
STATE_FILE = DATA / "state" / "discord.json"
SCRIPTS = REPO_ROOT / "automation" / "scripts"

sys.path.insert(0, str(SCRIPTS))
from discord_notify import load_env, send  # noqa: E402


def api(path, token):
    resp = requests.get(
        f"https://discord.com/api/v10{path}",
        headers={"Authorization": f"Bot {token}"},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def latest_selection_date():
    files = sorted(DATA.glob("selection-*.json"))
    if not files:
        return None
    return files[-1].stem.replace("selection-", "")


def main():
    load_env()
    token = os.environ.get("DISCORD_BOT_TOKEN")
    channel = os.environ.get("DISCORD_CHANNEL_ID")
    if not token or not channel:
        sys.exit("error: DISCORD_BOT_TOKEN / DISCORD_CHANNEL_ID not set")

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    last_id = state.get("last_id")

    query = f"?after={last_id}&limit=50" if last_id else "?limit=10"
    messages = api(f"/channels/{channel}/messages{query}", token)
    if not messages:
        return
    messages.sort(key=lambda m: int(m["id"]))
    state["last_id"] = messages[-1]["id"]
    # Persist the cursor BEFORE acting on messages: a concurrent/next run must
    # never re-process the same replies (duplicate drafts + duplicate PRs).
    STATE_FILE.write_text(json.dumps(state))

    date = latest_selection_date()
    for msg in messages:
        if msg["author"].get("bot"):
            continue
        content = msg["content"].strip()
        # A selection reply is digits/spaces/commas only, e.g. "1" or "1 3".
        if not re.fullmatch(r"[\d\s,，]+", content):
            continue
        ranks = sorted({int(n) for n in re.findall(r"\d+", content)})
        if not ranks or not date:
            continue
        send(f"✍️ 收到选题 {ranks}，开始写稿（每篇约 3-5 分钟）…")
        for rank in ranks:
            try:
                subprocess.run(
                    [str(SCRIPTS / "generate_deep_dive.sh"), date, str(rank)],
                    cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=900,
                )
                draft = REPO_ROOT / "automation" / "drafts" / f"deep-dive-{date}-rank{rank}.zh.md"
                pr = subprocess.run(
                    [sys.executable, str(SCRIPTS / "make_pr.py"), str(draft)],
                    cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=300,
                ).stdout.strip()
                send(f"📬 选题 {rank} 草稿已开 PR：{pr}\n手机上 Merge = 发布；要改就在 PR 留言。")
            except subprocess.CalledProcessError as exc:
                send(f"⚠️ 选题 {rank} 写稿失败：\n```{(exc.stderr or str(exc))[-500:]}```")

    STATE_FILE.write_text(json.dumps(state))
    print(f"[{datetime.now(timezone.utc).isoformat()}] processed up to {state['last_id']}")


if __name__ == "__main__":
    main()
