#!/usr/bin/env python3
"""Tell the owner what the pipeline skipped while the AI world was talking about it.

Two stories reached her before they reached the pipeline: Meta's Muse (a dead
source meant it arrived nine days late) and TypeSafe's Jev (fetched, but the
headline never said the name, so the selector passed). Sources and prompts are
now fixed; this is the check that notices the next one.

A story counts as hot if its names keep recurring across the pool (heat) or it
ran hot on Hacker News (score). If a hot item was neither selected today nor
covered in the past week, it is reported — with the selector's own reason when
it gave one.

    coverage_check.py [YYYY-MM-DD]   check that day (default: today, PT)
    coverage_check.py --quiet        print only, no Discord
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
HEAT_FLOOR = 3          # distinct sources, not raw mentions
SCORE_FLOOR = 300
LOOKBACK_DAYS = 7


def load(path: Path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def pool_items(date: str) -> list:
    d = load(DATA / f"pool-{date}.json", {})
    return d.get("items", d if isinstance(d, list) else [])


def selected_blob(date: str) -> str:
    """Everything the selector chose that day, as one searchable string."""
    d = load(DATA / f"selection-{date}.json", {})
    keep = {k: v for k, v in d.items() if k != "skipped_hot"}
    return json.dumps(keep, ensure_ascii=False).lower()


def recent_coverage(date: str) -> str:
    day = datetime.strptime(date, "%Y-%m-%d")
    out = []
    for back in range(1, LOOKBACK_DAYS + 1):
        out.append(selected_blob((day - timedelta(days=back)).strftime("%Y-%m-%d")))
    return " ".join(out)


PROMO = re.compile(r"disrupt|save up to|tickets|webinar|sponsored|join us|last chance|"
                   r"register now|早鸟|限时", re.I)


def is_hot(item: dict) -> bool:
    if PROMO.search(item.get("title", "")):
        return False          # conference ads repeat like news but are not news
    if item.get("heat", 0) >= HEAT_FLOOR:
        return True
    # A big Hacker News thread counts only when at least one other source
    # touched the same story; otherwise it is general tech, not our beat.
    return item.get("score", 0) >= SCORE_FLOOR and item.get("heat", 0) >= 2


def covered(item: dict, today_blob: str, week_blob: str) -> bool:
    """Covered if the URL was chosen, or if the distinctive names in its title
    already appear in what was chosen — a different article about the same
    story counts as covered."""
    url = (item.get("url") or "").lower()
    if url and url in today_blob:
        return True
    names = [n.lower() for n in item.get("hot_names", [])]
    if names and all(n in today_blob for n in names[:2]):
        return True
    if names and all(n in week_blob for n in names[:2]):
        return True
    return False


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    date = args[0] if args else datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    quiet = "--quiet" in sys.argv

    items = pool_items(date)
    if not items:
        print(f"{date}: no pool, nothing to check")
        return
    today_blob = selected_blob(date)
    if not today_blob or today_blob == "{}":
        print(f"{date}: no selection file yet, skipping")
        return
    week_blob = recent_coverage(date)
    reasons = {r.get("title", "").lower(): r.get("why_skipped", "")
               for r in load(DATA / f"selection-{date}.json", {}).get("skipped_hot", [])}

    missed, seen = [], set()
    for item in sorted(items, key=lambda i: -max(i.get("heat", 0), i.get("score", 0) // 40)):
        if not is_hot(item) or covered(item, today_blob, week_blob):
            continue
        key = tuple(item.get("hot_names") or [item.get("title", "")[:40]])
        if key in seen:
            continue
        seen.add(key)
        missed.append(item)

    if not missed:
        print(f"{date}: {len(items)} items in the pool, nothing hot was missed")
        return

    lines = [f"🔎 **{date} 选题漏报自查**：{len(missed)} 条热点没有入选，也没在近 7 天写过"]
    for m in missed[:6]:
        why = reasons.get((m.get("title") or "").lower(), "")
        heat = f"热度 {m.get('heat', 0)}" + (f" · HN {m['score']} 分" if m.get("score") else "")
        lines.append(f"· {m['title'][:76]}\n  {heat} · {m.get('source', '')}"
                     + (f"\n  选题时的理由：{why}" if why else ""))
    lines.append("想写哪条，回一句 `写 <关键词或链接>`。")
    text = "\n".join(lines)
    print(text)
    if not quiet:
        sys.path.insert(0, str(HERE))
        try:
            from discord_notify import send
            send(text)
        except Exception as exc:  # noqa: BLE001 — a failed notice must not fail the check
            print("discord notice failed:", str(exc)[:120])


if __name__ == "__main__":
    main()
