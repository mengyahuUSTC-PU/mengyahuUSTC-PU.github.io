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
    <date>.json       {"items": [...], "sent": {"zh": {...}}}  waiting / partly sent
    <date>.sent.json  the same after every language went out, with counts
    .lock             held for the whole of a send and of an enqueue

The two rules that matter, both learned the hard way: a list must never get
the same article twice, and a language that already went out must never be
resent because the other language failed.
"""

import fcntl
import html
import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
DIGEST_DIR = DATA / "newsletter-digest"
LOCAL_TZ = ZoneInfo("America/Los_Angeles")
SEND_HOUR = 23  # the digest goes out in the last hour of the local day
LANGS = ("zh", "en")


def now_local() -> datetime:
    return datetime.now(timezone.utc).astimezone(LOCAL_TZ)


@contextmanager
def locked():
    """enqueue and send hold the same lock, so an approval that lands while
    the send is in flight waits, then sees the digest as sent and rolls to
    tomorrow — instead of being written into a file that is about to be
    renamed away."""
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    with (DIGEST_DIR / ".lock").open("w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _load(path: Path) -> dict:
    """A digest file is {"items": [...], "sent": {...}}. Unreadable files are
    moved aside rather than crashing every nightly run."""
    if not path.exists():
        return {"items": [], "sent": {}}
    try:
        data = json.loads(path.read_text())
    except Exception:
        path.rename(path.with_suffix(".corrupt.json"))
        return {"items": [], "sent": {}}
    if isinstance(data, list):  # first-cut format
        data = {"items": data, "sent": {}}
    data.setdefault("items", [])
    data.setdefault("sent", {})
    return data


def _write(path: Path, data: dict):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)


def _sent_today(date: str) -> bool:
    return (DIGEST_DIR / f"{date}.sent.json").exists()


def _pending_files():
    return sorted(p for p in DIGEST_DIR.glob("????-??-??.json"))


def enqueue(slug: str, title: str, email: dict, url: str = "") -> str:
    """Add an article to the next digest. Returns the local date it will go
    out on: today, unless today's digest has already been sent."""
    with locked():
        now = now_local()
        target = now.date()
        if _sent_today(target.isoformat()):
            target = target + timedelta(days=1)
        path = DIGEST_DIR / f"{target.isoformat()}.json"

        # One copy anywhere: a 补发 after a failed night must not leave the
        # article in both yesterday's and today's file.
        for other in _pending_files():
            if other == path:
                continue
            data = _load(other)
            kept = [it for it in data["items"] if it["slug"] != slug]
            if len(kept) != len(data["items"]):
                if kept or data["sent"]:
                    _write(other, {**data, "items": kept})
                else:
                    other.unlink()

        data = _load(path)
        data["items"] = [it for it in data["items"] if it["slug"] != slug]  # re-approval replaces
        data["items"].append({"slug": slug, "title": title, "email": email, "url": url,
                              "queued_at": now.isoformat()})
        _write(path, data)
        return target.isoformat()


def compose(lang: str, items: list):
    """One article is sent as itself; several are stacked under their own
    headings, with the subject naming the first and counting the rest."""
    parts = [it for it in items if (it.get("email") or {}).get(lang, {}).get("html")
             and it["email"][lang].get("subject")]
    if not parts:
        return None, None
    if len(parts) == 1:
        e = parts[0]["email"][lang]
        return e["subject"], e["html"]

    first = parts[0]["email"][lang]["subject"]
    extra = len(parts) - 1
    subject = (f"{first}（另附 {extra} 篇）" if lang == "zh"
               else f"{first} (+{extra} more)")
    intro = ("<p>这封信里有 %d 篇新文章。</p>" % len(parts) if lang == "zh"
             else "<p>%d new pieces, bundled into one email.</p>" % len(parts))
    sections = []
    for it in parts:
        e = it["email"][lang]
        sections.append(f'<h2 style="font-size:1.15em;margin:1.6em 0 .4em">'
                        f'{html.escape(e["subject"])}</h2>\n{e["html"]}')
    return subject, intro + "\n<hr>\n".join(sections)


def pending_dates(today: str) -> list:
    """Unsent digests dated today or earlier: a day the cron missed (VM down,
    provider outage) is folded into the next send rather than dropped."""
    out = []
    for path in _pending_files():
        date = path.stem
        if date <= today and not _sent_today(date) and _load(path)["items"]:
            out.append(date)
    return out


def _merge(dates: list) -> tuple[list, dict]:
    """Items across the merged dates, one per slug (latest approval wins), and
    the union of what was already sent per language."""
    by_slug, sent = {}, {}
    for date in dates:
        data = _load(DIGEST_DIR / f"{date}.json")
        for it in data["items"]:
            prev = by_slug.get(it["slug"])
            if not prev or it.get("queued_at", "") >= prev.get("queued_at", ""):
                by_slug[it["slug"]] = it
        for lang, rec in data["sent"].items():
            sent[lang] = rec
    items = sorted(by_slug.values(), key=lambda it: it.get("queued_at", ""))
    return items, sent


def _mark_sent(dates: list, lang: str, rec: dict):
    """Persist a language's success the moment it happens, in every merged
    file, so a later failure in the other language cannot cause a resend."""
    for date in dates:
        path = DIGEST_DIR / f"{date}.json"
        data = _load(path)
        data["sent"][lang] = rec
        _write(path, data)


def send_due(force: bool = False) -> str:
    sys.path.insert(0, str(HERE))
    from resend_client import ResendError, preflight, send_newsletter

    with locked():
        now = now_local()
        today = now.date().isoformat()
        if now.hour != SEND_HOUR and not force:
            return f"not the sending hour (local {now:%H:%M}); nothing done"
        dates = pending_dates(today)
        if not dates:
            return "nothing queued"

        items, already = _merge(dates)
        ok, note = preflight()
        if not ok:
            return f"FAILED preflight, digest kept for next run: {note}"

        counts, failures = dict(), []
        for lang in LANGS:
            if lang in already:
                counts[lang] = already[lang].get("count", 0)
                continue  # went out on an earlier attempt tonight; never again
            subject, body = compose(lang, items)
            if not subject:
                _mark_sent(dates, lang, {"at": now.isoformat(), "count": 0, "note": "no content"})
                continue
            try:
                n = send_newsletter(lang, subject, body)
            except ResendError as exc:
                failures.append(f"{lang}: {exc}")
                continue
            except Exception as exc:  # noqa: BLE001 — keep the digest, report the cause
                failures.append(f"{lang}: {str(exc)[:200]}")
                continue
            counts[lang] = n
            _mark_sent(dates, lang, {"at": now.isoformat(), "count": n, "subject": subject})

        if failures:
            done = " · ".join(f"{l} 已发（{c} 人）" for l, c in counts.items() if l not in already or True)
            return ("FAILED send, digest kept for next run: " + " · ".join(failures) +
                    (f"\n已经发出去的不会重发：{done}" if counts else ""))

        record = {"sent_at": now.isoformat(), "counts": counts,
                  "articles": [it["slug"] for it in items], "merged_dates": dates}
        for date in dates:
            src = DIGEST_DIR / f"{date}.json"
            _write(DIGEST_DIR / f"{date}.sent.json", {**record, **_load(src)})
            src.unlink()
        titles = "、".join(f"《{it['title']}》" for it in items)
        parts = []
        for l in LANGS:
            if l in counts:
                parts.append(f"{l} → {counts[l]} 人" if counts[l] else f"{l} 无订阅者")
        return f"sent {len(items)} article(s) — {' · '.join(parts)}\n{titles}"


def status() -> str:
    lines = [f"local time {now_local():%Y-%m-%d %H:%M}"]
    for path in _pending_files():
        data = _load(path)
        sent = ", ".join(f"{l} sent" for l in data["sent"]) or "nothing sent yet"
        lines.append(f"  {path.stem}: {len(data['items'])} waiting ({sent}) — " +
                     ", ".join(it["slug"] for it in data["items"]))
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
    stamp = f"[{datetime.now(timezone.utc):%Y-%m-%d %H:%MZ} / {now_local():%H:%M} PT]"
    if cmd == "send":
        try:
            result = send_due(force="--force" in sys.argv)
        except Exception as exc:  # noqa: BLE001 — the cron must always report
            result = f"FAILED with an unexpected error, digest kept: {exc!r}"
        print(stamp, result)
        quiet = result.startswith(("not the sending hour", "nothing queued"))
        if not quiet:
            try:
                sys.path.insert(0, str(HERE))
                from discord_notify import send
                icon = "📧" if result.startswith("sent") else "🚨"
                send(f"{icon} **Newsletter 合集** {result}")
            except Exception:
                pass
    else:
        print(stamp, status())
