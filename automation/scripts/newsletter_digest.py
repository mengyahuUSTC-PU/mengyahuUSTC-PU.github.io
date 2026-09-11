#!/usr/bin/env python3
"""One newsletter a day, at most.

Approving two articles in one afternoon used to mean two emails an hour apart,
which reads as spam. Now approval only adds the article to the day's digest;
a cron near midnight Seattle time sends whatever accumulated as ONE email per
language, and anything that misses the cutoff rides along the next day.

    newsletter_digest.py send            send today's digest if it is 23:xx local
    newsletter_digest.py send --force    send now regardless of the hour
    newsletter_digest.py status          show what is queued and what was sent

State lives in automation/data/newsletter-digest/:
    <date>.json       items waiting for that local date
    <date>.sent.json  the same, after sending, with the counts
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
DIGEST_DIR = DATA / "newsletter-digest"
LOCAL_TZ = ZoneInfo("America/Los_Angeles")
SEND_HOUR = 23  # the digest goes out in the last hour of the local day


def now_local() -> datetime:
    return datetime.now(timezone.utc).astimezone(LOCAL_TZ)


def _load(path: Path) -> list:
    return json.loads(path.read_text()) if path.exists() else []


def _sent_today(date: str) -> bool:
    return (DIGEST_DIR / f"{date}.sent.json").exists()


def enqueue(slug: str, title: str, email: dict, url: str = "") -> str:
    """Add an article to the next digest. Returns the local date it will go
    out on: today, unless today's digest has already been sent."""
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    now = now_local()
    target = now.date()
    if _sent_today(target.isoformat()):
        target = target + timedelta(days=1)
    path = DIGEST_DIR / f"{target.isoformat()}.json"
    items = [it for it in _load(path) if it["slug"] != slug]  # re-approval replaces
    items.append({"slug": slug, "title": title, "email": email, "url": url,
                  "queued_at": now.isoformat()})
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2))
    return target.isoformat()


def compose(lang: str, items: list):
    """One article is sent as itself; several are stacked under their own
    headings, with the subject naming the first and counting the rest."""
    parts = [it for it in items if (it.get("email") or {}).get(lang, {}).get("html")]
    if not parts:
        return None, None
    if len(parts) == 1:
        e = parts[0]["email"][lang]
        return e["subject"], e["html"]

    first = parts[0]["email"][lang]["subject"]
    extra = len(parts) - 1
    subject = (f"{first}（另附 {extra} 篇）" if lang == "zh"
               else f"{first} (+{extra} more)")
    intro = ("<p>今天有 %d 篇新文章，合在一封里发给你。</p>" % len(parts) if lang == "zh"
             else "<p>%d new pieces today, bundled into one email.</p>" % len(parts))
    sections = []
    for it in parts:
        e = it["email"][lang]
        sections.append(f'<h2 style="font-size:1.15em;margin:1.6em 0 .4em">{e["subject"]}</h2>\n{e["html"]}')
    return subject, intro + "\n<hr>\n".join(sections)


def pending_dates(today: str) -> list:
    """Unsent digests dated today or earlier: a day the cron missed (VM down,
    provider outage) is folded into the next send rather than dropped."""
    out = []
    for path in sorted(DIGEST_DIR.glob("????-??-??.json")):
        date = path.stem
        if date <= today and not _sent_today(date) and _load(path):
            out.append(date)
    return out


def send_due(force: bool = False) -> str:
    sys.path.insert(0, str(HERE))
    from resend_client import ResendError, preflight, send_newsletter

    now = now_local()
    today = now.date().isoformat()
    if now.hour != SEND_HOUR and not force:
        return f"not the sending hour (local {now:%H:%M}); nothing done"
    dates = pending_dates(today)
    if not dates:
        return "nothing queued"

    items = []
    for date in dates:
        items += _load(DIGEST_DIR / f"{date}.json")
    ok, note = preflight()
    if not ok:
        return f"preflight failed, digest kept for next run: {note}"

    counts, failures = {}, []
    for lang in ("zh", "en"):
        subject, html = compose(lang, items)
        if not subject:
            continue
        try:
            counts[lang] = send_newsletter(lang, subject, html)
        except ResendError as exc:
            failures.append(f"{lang}: {exc}")
        except Exception as exc:  # noqa: BLE001 — keep the digest, report the cause
            failures.append(f"{lang}: {str(exc)[:200]}")

    if failures:
        return "send failed, digest kept for next run: " + " · ".join(failures)

    record = {"sent_at": now.isoformat(), "counts": counts,
              "articles": [it["slug"] for it in items], "merged_dates": dates}
    for date in dates:
        src = DIGEST_DIR / f"{date}.json"
        (DIGEST_DIR / f"{date}.sent.json").write_text(
            json.dumps({**record, "items": _load(src)}, ensure_ascii=False, indent=2))
        src.unlink()
    titles = "、".join(f"《{it['title']}》" for it in items)
    sent = " · ".join(f"{l} → {n} 人" for l, n in counts.items() if n)
    return f"sent {len(items)} article(s) — {sent}\n{titles}"


def status() -> str:
    lines = [f"local time {now_local():%Y-%m-%d %H:%M}"]
    for path in sorted(DIGEST_DIR.glob("????-??-??.json")):
        items = _load(path)
        lines.append(f"  {path.stem}: {len(items)} waiting — " +
                     ", ".join(it["slug"] for it in items))
    for path in sorted(DIGEST_DIR.glob("????-??-??.sent.json"))[-5:]:
        rec = json.loads(path.read_text())
        lines.append(f"  {path.stem.replace('.sent', '')}: sent {rec.get('counts')} "
                     f"({len(rec.get('articles', []))} article(s))")
    return "\n".join(lines)


def load_env(path=Path("/home/mia/site/.env")):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


if __name__ == "__main__":
    load_env()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "send":
        result = send_due(force="--force" in sys.argv)
        print(result)
        if result.startswith("sent") or result.startswith("send failed"):
            try:
                sys.path.insert(0, str(HERE))
                from discord_notify import send
                icon = "📧" if result.startswith("sent") else "🚨"
                send(f"{icon} **Newsletter 合集** {result}")
            except Exception:
                pass
    else:
        print(status())
