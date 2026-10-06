#!/usr/bin/env python3
"""One newsletter a week.

History: one email per approved article read as spam, so in 2026-09 approvals
were bundled into a nightly digest. That still tied email to 「发」: whenever
nothing was approved, subscribers heard nothing (two silent weeks in late
September). Since 2026-10 the owner chose a weekly letter: Sunday ~23:59
Seattle time, one email per language, carrying every deep dive that went live
that week, approved for social or not, plus the week's daily briefings as a
list of links.

    newsletter_digest.py send              send the week's letter if it is Sunday 23:xx
                                           local, or a missed one up to two days late
    newsletter_digest.py send --force      send the current week's letter now
    newsletter_digest.py preview [SUNDAY]  compose without sending; HTML goes to
                                           /tmp/newsletter-preview-<lang>.html
    newsletter_digest.py status            show what is queued and what was sent

State lives in automation/data/newsletter-digest/, one file per week, named
after the Sunday that closes it:
    <sunday>.json       {"items": [...], "sent": {"zh": {...}}}  queued / partly sent
    <sunday>.sent.json  the same after every language went out, with counts
    .lock               held for the whole of a send and of an enqueue
(Older files are dated per day, from the nightly-digest era; they are read
the same way.)

The two rules that matter, both learned the hard way: a list must never get
the same article twice, and a language that already went out must never be
resent because the other language failed.
"""

import fcntl
import html
import json
import os
import re
import sys
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
DIGEST_DIR = DATA / "newsletter-digest"
LOCAL_TZ = ZoneInfo("America/Los_Angeles")
SEND_HOUR = 23  # the letter goes out in the last hour of the local day
LATE_DAYS = 2   # a Sunday the cron missed is made up on Monday or Tuesday night
LOOKBACK_DAYS = 14  # how far back an unsent deep dive can still be picked up
LANGS = ("zh", "en")
REPO = HERE.parent.parent
SITE = "https://mengyahu.com"


def week_end(d):
    """The Sunday that closes the week containing d."""
    return d + timedelta(days=6 - d.weekday())


def last_week_end(d):
    """The most recent Sunday on or before d."""
    return d - timedelta(days=(d.weekday() + 1) % 7)


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


def enqueue(slug: str, title: str, email: dict, url: str = "", force: bool = False) -> str:
    """Make sure an article is in the next weekly letter (「发」 and 「补发」
    call this; deep dives that went live are also picked up without it).
    Returns the Sunday it will go out on: this week's, unless this week's
    letter has already been sent."""
    with locked():
        if not force and slug in _emailed_slugs():
            return "already"
        now = now_local()
        target = week_end(now.date())
        if _sent_today(target.isoformat()):
            target = target + timedelta(days=7)
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
                              "queued_at": now.isoformat(), "force": force})
        _write(path, data)
        return target.isoformat()


PODCAST_MANIFEST = Path("/home/mia/site/src/data/podcast.json")


def _listen_line(item: dict, lang: str) -> str:
    """A line pointing at the audio version, when one exists. Links to the
    article page (which carries the player), not to a bare mp3."""
    if lang != "zh":
        return ""
    try:
        episodes = json.loads(PODCAST_MANIFEST.read_text())
    except Exception:
        return ""
    ep = episodes.get(item["slug"])
    if not ep:
        return ""
    minutes = max(1, round(ep["seconds"] / 60))
    url = f"https://mengyahu.com/zh/{item['slug']}/"
    return (f'<p style="margin:.8em 0 0"><a href="{url}">🎧 听音频版（约 {minutes} 分钟）</a>'
            f' · <a href="https://mengyahu.com/zh/podcast/">订阅播客《胡说 AI》</a></p>')


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---"):
        return {}
    fm = text.split("---", 2)[1]
    out = {}
    for key in ("title", "pubDate", "lang", "draft"):
        m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    return out


def _emailed_slugs() -> set:
    """Every article any earlier letter carried, nightly or weekly."""
    seen = set()
    for path in DIGEST_DIR.glob("*.sent.json"):
        try:
            rec = json.loads(path.read_text())
        except Exception:
            continue
        seen.update(rec.get("articles", []))
        seen.update(it.get("slug") for it in rec.get("items", []) if isinstance(it, dict))
    return seen


def _briefing_title(title: str) -> str:
    return re.sub(r"^(AI 快讯[：:]\s*|AI briefing:\s*)", "", title).strip()


def collect_week(end, queued: list) -> tuple[list, dict]:
    """What the letter for the week ending `end` carries.

    Deep dives: everything queued, plus every deep dive that went live in the
    lookback window and was never emailed; one per slug, newest first.
    Briefings: the week's daily briefings per language, oldest first."""
    from datetime import date as _date
    start = end - timedelta(days=6)
    floor = end - timedelta(days=LOOKBACK_DAYS - 1)
    emailed = _emailed_slugs()
    by_slug = {it["slug"]: it for it in queued
               if it.get("force") or it["slug"] not in emailed}
    for md in sorted((REPO / "src" / "content" / "blog" / "zh").glob("*.md")):
        slug = md.stem
        if slug.startswith("briefing") or slug in by_slug or slug in emailed:
            continue
        fm = _frontmatter(md)
        try:
            pub = _date.fromisoformat(fm.get("pubDate", "")[:10])
        except ValueError:
            continue
        if fm.get("draft") == "true" or not (floor <= pub <= end):
            continue
        pack_path = DATA / "dist" / f"{slug}.json"
        if not pack_path.exists():
            continue  # no newsletter copy yet (English version not live)
        pack = json.loads(pack_path.read_text())
        if not pack.get("email"):
            continue
        by_slug[slug] = {"slug": slug, "title": fm.get("title", slug), "email": pack["email"],
                         "pubDate": pub.isoformat(), "auto": True}
    for it in by_slug.values():
        if "pubDate" not in it:
            fm = _frontmatter(REPO / "src" / "content" / "blog" / "zh" / f"{it['slug']}.md") \
                if (REPO / "src" / "content" / "blog" / "zh" / f"{it['slug']}.md").exists() else {}
            it["pubDate"] = fm.get("pubDate", "")[:10]
    items = sorted(by_slug.values(), key=lambda it: it.get("pubDate", ""), reverse=True)

    briefings = {}
    for lang in LANGS:
        rows = []
        for md in sorted((REPO / "src" / "content" / "blog" / lang).glob("briefing-*.md")):
            fm = _frontmatter(md)
            try:
                pub = _date.fromisoformat(fm.get("pubDate", "")[:10])
            except ValueError:
                continue
            if start <= pub <= end and fm.get("draft") != "true":
                url = (f"{SITE}/{lang}/{md.stem}/?utm_source=newsletter&utm_medium=email"
                       f"&utm_campaign=weekly-{end.isoformat()}")
                rows.append({"slug": md.stem, "date": pub.isoformat(),
                             "title": _briefing_title(fm.get("title", md.stem)), "url": url})
        briefings[lang] = rows
    return items, briefings


def _week_label(lang: str, end) -> str:
    start = end - timedelta(days=6)
    if lang == "zh":
        return f"{start.month}/{start.day}–{end.month}/{end.day}"
    if start.month == end.month:
        return f"{start:%b} {start.day}–{end.day}"
    return f"{start:%b} {start.day} – {end:%b} {end.day}"


def compose(lang: str, items: list, briefings: list = (), end=None):
    """The week's deep dives (each as its own newsletter copy), then the
    week's briefings as a list of links. The subject is the newest deep
    dive's, counting the rest; a week with briefings only is named by date."""
    from datetime import date as _date
    parts = [it for it in items if (it.get("email") or {}).get(lang, {}).get("html")
             and it["email"][lang].get("subject")]
    briefings = list(briefings or [])
    if not parts and not briefings:
        return None, None
    end = end or week_end(now_local().date())

    if parts:
        first = parts[0]["email"][lang]["subject"]
        extra = len(parts) - 1
        subject = first if not extra else (f"{first}（另附 {extra} 篇）" if lang == "zh"
                                           else f"{first} (+{extra} more)")
    else:
        subject = (f"本周 AI 快讯（{_week_label(lang, end)}）" if lang == "zh"
                   else f"This week in AI ({_week_label(lang, end)})")

    sections = []
    if len(parts) == 1:
        e = parts[0]["email"][lang]
        sections.append(e["html"] + _listen_line(parts[0], lang))
    elif parts:
        intro = (f"<p>这周有 {len(parts)} 篇新文章。</p>" if lang == "zh"
                 else f"<p>{len(parts)} new pieces this week.</p>")
        blocks = []
        for it in parts:
            e = it["email"][lang]
            blocks.append(f'<h2 style="font-size:1.15em;margin:1.6em 0 .4em">'
                          f'{html.escape(e["subject"])}</h2>\n{e["html"]}{_listen_line(it, lang)}')
        sections.append(intro + "\n<hr>\n".join(blocks))
    if briefings:
        head = "本周快讯" if lang == "zh" else "This week's briefings"
        rows = []
        for b in briefings:
            d = _date.fromisoformat(b["date"])
            label = f"{d.month}/{d.day}" if lang == "zh" else f"{d:%b} {d.day}"
            rows.append(f'<li style="margin:.35em 0"><span style="color:#888">{label}</span> '
                        f'<a href="{html.escape(b["url"])}">{html.escape(b["title"])}</a></li>')
        sections.append(f'<h2 style="font-size:1.15em;margin:1.6em 0 .4em">{head}</h2>\n'
                        f'<ul style="padding-left:1.2em">{"".join(rows)}</ul>')
    return subject, "\n<hr>\n".join(sections)


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
        today = now.date()
        if force:
            end = week_end(today)
        else:
            if now.hour != SEND_HOUR:
                return f"not the sending hour (local {now:%H:%M}); nothing done"
            end = last_week_end(today)
            if (today - end).days > LATE_DAYS:
                return f"not a sending day (local {now:%a}); the letter goes out Sunday 23:59"
        key = end.isoformat()
        if _sent_today(key):
            return "nothing queued"  # this week's letter already went out
        dates = pending_dates(key)
        if key not in dates:
            dates.append(key)  # the week's own file carries the per-language sent marks
        queued, already = _merge(dates)
        items, briefings = collect_week(end, queued)
        if not items and not any(briefings.values()):
            return "nothing queued"
        ok, note = preflight()
        if not ok:
            return f"FAILED preflight, letter kept for next run: {note}"

        counts, failures = dict(), []
        for lang in LANGS:
            if lang in already:
                counts[lang] = already[lang].get("count", 0)
                continue  # went out on an earlier attempt; never again
            subject, body = compose(lang, items, briefings.get(lang, []), end)
            if not subject:
                _mark_sent(dates, lang, {"at": now.isoformat(), "count": 0, "note": "no content"})
                continue
            try:
                n = send_newsletter(lang, subject, body)
            except ResendError as exc:
                failures.append(f"{lang}: {exc}")
                continue
            except Exception as exc:  # noqa: BLE001 — keep the letter, report the cause
                failures.append(f"{lang}: {str(exc)[:200]}")
                continue
            counts[lang] = n
            _mark_sent(dates, lang, {"at": now.isoformat(), "count": n, "subject": subject})

        if failures:
            done = " · ".join(f"{l} 已发（{c} 人）" for l, c in counts.items())
            return ("FAILED send, letter kept for next run: " + " · ".join(failures) +
                    (f"\n已经发出去的不会重发：{done}" if counts else ""))

        record = {"sent_at": now.isoformat(), "counts": counts, "week_end": key,
                  "articles": [it["slug"] for it in items],
                  "briefings": {l: [b["slug"] for b in briefings.get(l, [])] for l in LANGS},
                  "merged_dates": dates}
        week_state = _load(DIGEST_DIR / f"{key}.json")
        _write(DIGEST_DIR / f"{key}.sent.json", {**record, **week_state, "items": items})
        for date in dates:
            src = DIGEST_DIR / f"{date}.json"
            if src.exists():
                src.unlink()
        titles = "、".join(f"《{it['title']}》" for it in items) or "（本周没有深度文章）"
        parts = []
        for l in LANGS:
            if l in counts:
                parts.append(f"{l} → {counts[l]} 人" if counts[l] else f"{l} 无订阅者")
        nb = len(briefings.get("zh", []))
        return (f"sent {len(items)} article(s) + {nb} briefing(s) — {' · '.join(parts)}\n{titles}")


def preview(end=None) -> str:
    """Compose the week's letter without sending; write the HTML to /tmp."""
    from datetime import date as _date
    end = _date.fromisoformat(end) if end else week_end(now_local().date())
    dates = pending_dates(end.isoformat())
    queued, _ = _merge(dates)
    items, briefings = collect_week(end, queued)
    lines = [f"week ending {end} — {len(items)} deep dive(s): " + ", ".join(it["slug"] for it in items)]
    for lang in LANGS:
        subject, body = compose(lang, items, briefings.get(lang, []), end)
        if not subject:
            lines.append(f"  {lang}: nothing to send")
            continue
        out = Path(f"/tmp/newsletter-preview-{lang}.html")
        out.write_text(f"<h3>{html.escape(subject)}</h3>\n{body}")
        lines.append(f"  {lang}: {subject!r} · {len(briefings.get(lang, []))} briefing(s) · {out}")
    return "\n".join(lines)


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
    if cmd == "preview":
        print(stamp, preview(sys.argv[2] if len(sys.argv) > 2 else None))
    elif cmd == "send":
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
                send(f"{icon} **每周 Newsletter** {result}")
            except Exception:
                pass
    else:
        print(stamp, status())
