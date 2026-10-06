#!/usr/bin/env python3
"""Nudge once, then let go, for distribution packs nobody approved.

A pack waits for 「发」 after the English version goes live. Some articles are
deliberately not posted to LinkedIn, so nothing is ever posted automatically
(owner's decision, 2026-10-05). Instead: one Discord reminder after 48 hours,
and after 7 days the pack is marked expired, so the weekly report stops
carrying it as a backlog. An expired pack can still be sent with 「发 <slug>」.

Run hourly from cron. Packs written before 2026-10-05 carry no previewed_at;
their file mtime stands in for it.
"""

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DIST = REPO_ROOT / "automation" / "data" / "dist"
sys.path.insert(0, str(REPO_ROOT / "automation" / "scripts"))
from discord_notify import load_env, send  # noqa: E402

REMIND_AFTER = timedelta(hours=48)
EXPIRE_AFTER = timedelta(days=7)


def _title(slug: str) -> str:
    md = REPO_ROOT / "src" / "content" / "blog" / "zh" / f"{slug}.md"
    if md.exists():
        m = re.search(r'^title:\s*"?(.*?)"?\s*$', md.read_text(), re.M)
        if m:
            return m.group(1)
    return slug


def _previewed_at(path: Path, pack: dict) -> datetime:
    if pack.get("previewed_at"):
        return datetime.fromisoformat(pack["previewed_at"])
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)


def _write(path: Path, pack: dict):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(pack, ensure_ascii=False, indent=2))
    tmp.replace(path)


def run(now: datetime | None = None, notify=send) -> list[str]:
    now = now or datetime.now(timezone.utc)
    log = []
    for path in sorted(DIST.glob("*.json")):
        try:
            pack = json.loads(path.read_text())
        except Exception:
            continue
        if pack.get("status") != "pending":
            continue
        slug = pack.get("slug") or path.stem
        age = now - _previewed_at(path, pack)
        if age >= EXPIRE_AFTER:
            pack["status"] = "expired"
            pack["expired_at"] = now.isoformat()
            _write(path, pack)
            log.append(f"expired {slug}")
        elif age >= REMIND_AFTER and not pack.get("reminded_at"):
            notify(f"⏰ 《{_title(slug)}》的英文版两天前上线了，LinkedIn 还没发。"
                   f"要发就回「定时发 {slug}」或「发 {slug}」；不想发就不用管，7 天后自动作废。")
            pack["reminded_at"] = now.isoformat()
            _write(path, pack)
            log.append(f"reminded {slug}")
    return log


if __name__ == "__main__":
    load_env()
    for line in run():
        print(f"[{datetime.now(timezone.utc):%Y-%m-%d %H:%MZ}] {line}")
