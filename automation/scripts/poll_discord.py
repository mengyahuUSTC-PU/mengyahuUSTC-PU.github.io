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

# Prompts are read once at import (from the master checkout) so that branch
# switches inside handlers can't hit branches that predate these files.
_P = REPO_ROOT / "automation" / "prompts"
_PROMPTS_CACHE = {
    "baseline": (_P / "editorial-baseline.md").read_text(),
    "lessons": (_P / "editorial-lessons.md").read_text(),
    "revise": (_P / "revise.md").read_text(),
}


def api(path, token):
    resp = requests.get(
        f"https://discord.com/api/v10{path}",
        headers={"Authorization": f"Bot {token}"},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def sh(*cmd, timeout=300):
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=timeout
    ).stdout.strip()


def handle_revision(slug: str, feedback: str):
    """Revise an article per Discord feedback and push to its PR branch.

    Open PR on post/<slug> -> revise on that branch (PR updates in place).
    No open PR but article published on master -> new fix/<slug> branch + PR.
    """
    lang = "en" if slug.endswith("-en") else "zh"
    base_slug = slug.removesuffix("-en")
    branch = f"post/{slug}"
    rel = f"src/content/blog/{lang}/{base_slug}.md"

    sh("git", "fetch", "-q", "origin")
    open_prs = json.loads(sh("gh", "pr", "list", "--state", "open",
                             "--json", "headRefName"))
    on_open_pr = any(p["headRefName"] == branch for p in open_prs)

    if on_open_pr:
        sh("git", "checkout", "-q", "-B", branch, f"origin/{branch}")
    else:
        sh("git", "checkout", "-q", "master")
        sh("git", "pull", "-q", "origin", "master")
        if not (REPO_ROOT / rel).exists():
            send(f"⚠️ 找不到 {slug} 对应的文章（{rel}），也没有它的开放 PR。")
            return
        branch = f"fix/{slug}-{datetime.now(timezone.utc).strftime('%m%d%H%M')}"
        sh("git", "checkout", "-q", "-B", branch, "origin/master")

    article = (REPO_ROOT / rel).read_text()
    send(f"✏️ 收到对 {slug} 的修改意见，改稿中…")
    prompt = (
        _PROMPTS_CACHE["baseline"]
        + "\n\n" + _PROMPTS_CACHE["lessons"]
        + "\n\n" + _PROMPTS_CACHE["revise"]
        + "\n\n## 用户修改意见\n\n" + feedback
        + "\n\n## 文章当前版本\n\n" + article
    )
    run = subprocess.run(
        ["claude", "-p", "--output-format", "text",
         "--model", "fable", "--fallback-model", "opus",
         "--allowedTools", "WebFetch", "WebSearch"],
        input=prompt, cwd=REPO_ROOT, capture_output=True, text=True, timeout=900,
    )
    if run.returncode != 0:
        send(f"⚠️ 改稿失败（{slug}）：\n```{(run.stderr or run.stdout)[-400:]}```")
        return
    clean = subprocess.run(
        [sys.executable, str(SCRIPTS / "split_output.py"), "json"],
        input=run.stdout, capture_output=True, text=True, check=True,
    ).stdout
    if not clean.strip().startswith("---"):
        send(f"⚠️ 改稿输出格式异常（{slug}），未提交。")
        return
    from sync_pair import revision_output_ok
    if not revision_output_ok(rel, article, clean):
        send(f"⚠️ 改稿产出疑似写成了另一语言或改了 lang/slug，已拒绝写入 {rel}。请确认意见针对的语言版本后重试。")
        return
    if sh("git", "rev-parse", "--abbrev-ref", "HEAD") != branch:
        send(f"⚠️ git 状态异常（不在 {branch} 上），改稿未提交，请重试。")
        return
    (REPO_ROOT / rel).write_text(clean)
    sh("git", "add", rel)
    sh("git", "commit", "-q", "-m",
       f"Revise {base_slug} ({lang}) per Discord feedback\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>")
    sh("git", "push", "-q", "-f", "origin", branch)
    try:
        from sync_pair import sync_counterpart
        if sync_counterpart(branch, rel):
            send("🔁 另一语言版本已同步同样的修改。")
    except Exception as exc:
        send(f"⚠️ 双语同步失败（需人工检查另一版）：{str(exc)[:200]}")

    if on_open_pr:
        send(f"✅ {slug} 已按意见改好，PR 原地更新，刷新即可复审。")
    else:
        pr_url = sh("gh", "pr", "create", "--base", "master", "--head", branch,
                    "--title", f"Revise: {slug} (Discord feedback)",
                    "--body", f"按 Discord 反馈修改：\n\n> {feedback}\n\nMerge = 修正上线。\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)")
        send(f"✅ {slug} 已按意见改好（该文已上线，走修正 PR）：{pr_url}")
    sh("git", "checkout", "-q", "master")
    try:
        from editorial_memory import update_lessons
        update_lessons(feedback, datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    except Exception:
        pass


def handle_distribution(slug: str, when: str = "now"):
    """Schedule the pending thread + LinkedIn drafts for next UTC 15:00."""
    from datetime import timedelta

    from typefully_client import create_draft

    dist_file = DATA / "dist" / f"{slug}.json"
    if not dist_file.exists():
        send(f"⚠️ 找不到 {slug} 的分发内容（automation/data/dist/{slug}.json）。")
        return
    pack = json.loads(dist_file.read_text())
    if pack.get("status") == "scheduled":
        send(f"ℹ️ {slug} 已经排程过了，跳过。")
        return

    # Default: publish immediately on approval (user decision 2026-07-19,
    # freshness first). "定时发" instead targets the next weekday peak slots.
    from datetime import timedelta

    if when == "peak":
        # Weekends included: the user's own data shows solid weekend traffic.
        def next_peak(hour_utc: int) -> str:
            slot = datetime.now(timezone.utc).replace(
                hour=hour_utc, minute=0, second=0, microsecond=0)
            while slot <= datetime.now(timezone.utc):
                slot += timedelta(days=1)
            return slot.strftime("%Y-%m-%dT%H:%M:%SZ")
        x_when, li_when = next_peak(16), next_peak(20)
    else:
        # X policy forbids DIRECT publishing of URL-carrying drafts via API
        # (403 FORBIDDEN); a near-future schedule is "immediate" in practice
        # but goes through the allowed scheduling path.
        soon = (datetime.now(timezone.utc) + timedelta(minutes=2)).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        x_when = li_when = soon

    try:
        create_draft(thread=[pack["thread"].strip()], publish_at=x_when, title=f"{slug} (X)")
        create_draft(linkedin=pack["linkedin"], publish_at=li_when,
                     title=f"{slug} (LinkedIn)")
    except Exception as exc:
        send(f"⚠️ Typefully 发布失败（{slug}）：{str(exc)[:300]}")
        return

    pack["status"] = "scheduled"
    pack["scheduled_for"] = {"x": x_when, "linkedin": li_when,
                             "at": datetime.now(timezone.utc).isoformat()}
    dist_file.write_text(json.dumps(pack, ensure_ascii=False, indent=2))

    # Newsletter: same approval gate as Typefully ("发" = user reviewed the pack).
    # A failure here must never read as success — the social posts going out
    # while the email silently dies is exactly what happened on 2026-08-25.
    newsletter_status = "未生成"
    if pack.get("email"):
        # Kit's free plan blocks POST /broadcasts, so Kit is only the signup form
        # and the list of record now; Resend does the sending.
        from resend_client import ResendError, preflight, send_newsletter
        counts, failures = {}, []
        allowed, note = preflight()
        if not allowed:
            failures.append(f"Resend 预检未通过：{note}")
        else:
            for lang in ("zh", "en"):
                part = pack["email"].get(lang) or {}
                if not (part.get("subject") and part.get("html")):
                    continue
                try:
                    counts[lang] = send_newsletter(lang, part["subject"], part["html"])
                except ResendError as exc:
                    failures.append(f"{lang}: {exc}")
                except Exception as exc:
                    failures.append(f"{lang}: {str(exc)[:200]}")
        if failures:
            # Keep the rendered email so nothing has to be regenerated: the user
            # can paste it into Kit's dashboard, or resend once Kit is fixed.
            outbox = REPO_ROOT / "automation" / "data" / "newsletter-unsent"
            outbox.mkdir(parents=True, exist_ok=True)
            saved = []
            for lang in ("zh", "en"):
                part = pack["email"].get(lang) or {}
                if not (part.get("subject") and part.get("html")):
                    continue
                path = outbox / f"{slug}.{lang}.html"
                path.write_text(f"<!-- subject: {part['subject']} -->\n{part['html']}")
                saved.append(str(path))
            newsletter_status = "❌ 未发出"
            send("🚨 **Newsletter 没有发出去**（{}）\n原因：{}\n"
                 "邮件正文已存好，不用重新生成：\n{}\n"
                 "邮件没丢，修好后回一句「补发 {}」就行。".format(slug, 
                     " · ".join(failures)[:400], "\n".join(saved), slug))
        else:
            sent = [f"{l} → {n} 人" for l, n in counts.items() if n]
            if sent:
                newsletter_status = "✅ " + " · ".join(sent)
                send(f"📧 Newsletter 已发出（Resend）：{' · '.join(sent)}")
            elif counts:
                newsletter_status = "⏭ 无订阅者"
                send("📧 Newsletter 跳过：目前还没有订阅者。")
    if when == "peak":
        from zoneinfo import ZoneInfo
        def pt(s):
            d = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            return d.astimezone(ZoneInfo("America/Los_Angeles")).strftime("%m-%d %H:%M")
        send(f"⏰ {slug} 已排进高峰时段（西雅图时间）：X → {pt(x_when)} · LinkedIn → {pt(li_when)}。")
    else:
        send(f"🚀 {slug} 的 X 帖 + LinkedIn 帖已排程，2 分钟后自动发出（X 政策不允许 API 带链接直发，走排程通道效果相同）。")

    # One closing line that states every channel, so a partial failure can never
    # be mistaken for a clean send.
    send(f"📋 **{slug} 分发结果**：X ✅ · LinkedIn ✅ · Newsletter {newsletter_status}")


def handle_newsletter_resend(slug: str):
    """"补发 <slug>": send the newsletter for an already-distributed pack.

    Used after a send failed (bad key, unverified domain, provider outage). The
    social posts are untouched — this only pushes the email.
    """
    dist_file = DATA / "dist" / f"{slug}.json"
    if not dist_file.exists():
        send(f"⚠️ 找不到 {slug} 的分发包。")
        return
    pack = json.loads(dist_file.read_text())
    email = pack.get("email") or {}
    if not email:
        send(f"⚠️ {slug} 没有 newsletter 内容。")
        return

    from resend_client import ResendError, preflight, send_newsletter
    allowed, note = preflight()
    if not allowed:
        send(f"⚠️ 还是发不了：{note}")
        return

    counts, failures = {}, []
    for lang in ("zh", "en"):
        part = email.get(lang) or {}
        if not (part.get("subject") and part.get("html")):
            continue
        try:
            counts[lang] = send_newsletter(lang, part["subject"], part["html"])
        except ResendError as exc:
            failures.append(f"{lang}: {exc}")
        except Exception as exc:
            failures.append(f"{lang}: {str(exc)[:200]}")

    if failures:
        send(f"🚨 补发失败（{slug}）：{' · '.join(failures)[:400]}")
        return
    sent = " · ".join(f"{l} → {n} 人" for l, n in counts.items() if n)
    send(f"📧 {slug} 的 newsletter 已补发：{sent or '没有订阅者'}")


HELP_TEXT = ("🤔 没听懂。可用指令：\n"
             "`1 3` 选题 · `写 话题或链接` 手动选题 · `改文章 [slug] 意见` · `改简报 意见` · "
             "`改L 意见`（LinkedIn）· `改X 意见`（thread）· `发 [slug]` 排程 · "
             "`补发 [slug]` 重发 newsletter · `退订 <邮箱>`")


def latest_briefing_slug():
    posts = sorted((REPO_ROOT / "src" / "content" / "blog" / "zh").glob("briefing-*.md"))
    return posts[-1].stem if posts else None


def latest_article_slug():
    posts = [p for p in (REPO_ROOT / "src" / "content" / "blog" / "zh").glob("*.md")
             if not p.stem.startswith("briefing-") and p.stem != "hello-world"]
    if not posts:
        return None
    return max(posts, key=lambda p: p.stat().st_mtime).stem


def ask_which_pack(pending, cmd_hint):
    """Never guess between multiple pending packs — a wrong guess once mixed
    two same-evening articles' distribution content. Ask the user instead."""
    send("❓ 现在有多篇待发布的分发内容，你指的是哪一篇？\n"
         + "\n".join(f"- `{s}`" for s in pending)
         + f"\n请点名重发指令，例如 `{cmd_hint}`。")


def handle_dist_edit(part: str, feedback: str):
    """Revise only one part (thread/linkedin) of the pending dist pack."""
    pending_packs = []
    for f in sorted((DATA / "dist").glob("*.json"), key=lambda p: p.stat().st_mtime):
        try:
            d = json.loads(f.read_text())
            if d.get("status") != "scheduled":
                pending_packs.append(d)
        except Exception:
            continue
    if not pending_packs:
        send("⚠️ 没有待发布的分发内容。")
        return
    if len(pending_packs) > 1:
        ask_which_pack([d["slug"] for d in pending_packs], "改发 <slug> 意见")
        return
    pack = pending_packs[-1]
    slug = pack["slug"]
    label = "LinkedIn 帖" if part == "linkedin" else "X thread"
    fb = (f"只修改 {label}，另一部分必须原样保留。上一版内容如下：\n\n"
          f"===THREAD===\n{pack['thread']}\n===LINKEDIN===\n{pack['linkedin']}\n\n"
          f"用户意见：{feedback}")
    send(f"✏️ 收到，只改 {slug} 的 {label}…")
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "distribute.py"), slug, fb],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=1200,
    )
    if r.returncode != 0:
        send(f"⚠️ {label} 修改失败：\n```{(r.stderr or r.stdout)[-400:]}```")


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

        # "定时发 …": queue for next weekday peak slots instead of publishing now.
        peak_match = re.match(r"定时发[\s，,]*([A-Za-z0-9\- ]*)$", content)
        if peak_match:
            pending = []
            for f in sorted((DATA / "dist").glob("*.json"), key=lambda p: p.stat().st_mtime):
                try:
                    d = json.loads(f.read_text())
                    if d.get("status") != "scheduled":
                        pending.append(d["slug"])
                except Exception:
                    continue
            tokens = peak_match.group(1).split()
            slug_ = next((s for s in pending if s in tokens), None)
            if not slug_ and len(pending) == 1:
                slug_ = pending[0]
            if not slug_ and len(pending) > 1:
                ask_which_pack(pending, "定时发 <slug>")
                continue
            if slug_:
                handle_distribution(slug_, when="peak")
            else:
                send("ℹ️ 没有待排程的分发内容。")
            continue

        # "发 …": schedule a pending distribution pack via Typefully.
        # Accepts "发", "发 <slug>", or loose phrasing like "发 x linkedin" —
        # a token matching a pending pack slug wins, else the latest pending pack.
        dist_match = re.match(r"发[\s，,]*([A-Za-z0-9\- ]*)$", content)
        if dist_match:
            pending = []
            for f in sorted((DATA / "dist").glob("*.json"), key=lambda p: p.stat().st_mtime):
                try:
                    d = json.loads(f.read_text())
                    if d.get("status") != "scheduled":
                        pending.append(d["slug"])
                except Exception:
                    continue
            tokens = dist_match.group(1).split()
            slug_ = next((s for s in pending if s in tokens), None)
            if not slug_ and len(pending) == 1:
                slug_ = pending[0]
            if not slug_ and len(pending) > 1:
                ask_which_pack(pending, "发 <slug>")
                continue
            if slug_:
                handle_distribution(slug_)
            else:
                send("ℹ️ 没有待排程的分发内容（都已排程或尚未生成）。")
            continue

        # "退订 <email>": honour an opt-out that arrived as a reply.
        m = re.fullmatch(r"退订\s*[:：]?\s*(\S+@\S+)", content)
        if m:
            from resend_client import unsubscribe
            address = m.group(1).strip("<>")
            send(f"✅ {address} {unsubscribe(address)}")
            continue

        # "补发 [slug]": resend a newsletter whose delivery failed earlier.
        m = re.fullmatch(r"补发\s*([A-Za-z0-9\-]*)", content)
        if m:
            slug_ = m.group(1) or latest_article_slug()
            if slug_:
                handle_newsletter_resend(slug_)
            else:
                send("⚠️ 不知道补发哪一篇，带上 slug：`补发 <slug>`")
            continue

        # "改简报 [date] <feedback>": revise the latest (or dated) briefing.
        m = re.fullmatch(r"改简报\s*(\d{4}-\d{2}-\d{2})?[\s，,:：]*(.+)", content, re.S)
        if m:
            bdate = m.group(1) or latest_briefing_slug()
            if bdate:
                slug_ = bdate if bdate.startswith("briefing-") else f"briefing-{bdate}"
                handle_revision(slug_, m.group(2).strip())
            else:
                send("⚠️ 找不到任何简报，无法修改。")
            continue

        # "改文章 [slug] <feedback>": revise the latest (or named) deep-dive article.
        m = re.fullmatch(r"改文章\s*([A-Za-z0-9\-]*)[\s，,:：]*(.+)", content, re.S)
        if m:
            slug_ = m.group(1) or latest_article_slug()
            if slug_:
                handle_revision(slug_, m.group(2).strip())
            else:
                send("⚠️ 找不到目标文章，请带上 slug：`改文章 <slug> 意见`")
            continue

        # "改L <feedback>" / "改X <feedback>": revise one part of the latest dist pack.
        m = re.fullmatch(r"改\s*[LlＬ]\s*[\s，,:：]*(.+)", content, re.S) or \
            re.fullmatch(r"改领英[\s，,:：]*(.+)", content, re.S)
        if m:
            handle_dist_edit("linkedin", m.group(1).strip())
            continue
        m = re.fullmatch(r"改\s*[XxＸ推]\s*[\s，,:：]*(.+)", content, re.S)
        if m:
            handle_dist_edit("thread", m.group(1).strip())
            continue

        # "改发 <slug> <feedback>": regenerate distribution pack per feedback.
        redist_match = re.fullmatch(r"改发\s*([A-Za-z0-9\-]+)[\s，,:：]*(.+)", content, re.S)
        if redist_match:
            slug_, fb_ = redist_match.group(1), redist_match.group(2).strip()
            send(f"✏️ 收到对 {slug_} 分发内容的意见，重新生成中…")
            r = subprocess.run(
                [sys.executable, str(SCRIPTS / "distribute.py"), slug_, fb_],
                cwd=REPO_ROOT, capture_output=True, text=True, timeout=1200,
            )
            if r.returncode != 0:
                send(f"⚠️ 分发内容重生成失败：\n```{(r.stderr or r.stdout)[-400:]}```")
            continue

        # "改 <slug> <feedback>": revise the article per user feedback.
        revise_match = re.fullmatch(r"改\s*([A-Za-z0-9\-]+)[\s，,:：]*(.+)", content, re.S)
        if revise_match:
            handle_revision(revise_match.group(1), revise_match.group(2).strip())
            continue

        # "写 <topic>" / "深挖 <topic>": user-supplied topic outside the daily
        # candidate pool (e.g. news the user read elsewhere, or a pasted link).
        topic_match = re.fullmatch(r"(?:写|深挖)[\s，,:：]+(.+)", content, re.S)
        if topic_match:
            handle_new_topic(topic_match.group(1).strip())
            continue

        # A selection reply is digits/spaces/commas only, e.g. "1" or "1 3".
        if re.fullmatch(r"[\d\s,，]+", content):
            ranks = sorted({int(n) for n in re.findall(r"\d+", content)})
            if ranks and date:
                handle_selection(ranks, date)
            continue

        # Anything else: LLM router as fallback; never fail silently.
        try:
            acted = route_free_text(content, date)
        except Exception:
            acted = False
        if not acted and len(content) > 5:
            send(HELP_TEXT)


def handle_selection(ranks, date):
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
                send(f"📬 选题 {rank} 草稿已开 PR：{pr}\n随便迭代（PR 留言或「改」指令），满意后 Merge——之后核查、修正、英文版直到上线**全自动**，你只需在分发预览后回「发」。")
            except subprocess.CalledProcessError as exc:
                send(f"⚠️ 选题 {rank} 写稿失败：\n```{(exc.stderr or str(exc))[-500:]}```")


def handle_new_topic(topic: str):
    """Write a deep dive for a user-supplied topic (not in the candidate pool)."""
    send(f"✍️ 收到手动选题，先查证一手来源再写稿（约 5-8 分钟）…\n> {topic[:300]}")
    try:
        run = subprocess.run(
            [str(SCRIPTS / "generate_deep_dive.sh"), "--topic", topic],
            cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=1800,
        )
        draft_rel = run.stdout.strip().splitlines()[-1].removeprefix("wrote ").strip()
        pr = subprocess.run(
            [sys.executable, str(SCRIPTS / "make_pr.py"), str(REPO_ROOT / draft_rel)],
            cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=300,
        ).stdout.strip()
        send(f"📬 手动选题草稿已开 PR：{pr}\n随便迭代（PR 留言或「改」指令），满意后 Merge——之后核查、修正、英文版直到上线**全自动**，你只需在分发预览后回「发」。")
    except subprocess.CalledProcessError as exc:
        send(f"⚠️ 手动选题写稿失败：\n```{(exc.stderr or str(exc))[-500:]}```")


def route_free_text(content, date):
    """Classify a free-form message and dispatch. Silent on unrelated chatter."""
    open_prs = json.loads(sh("gh", "pr", "list", "--state", "open",
                             "--json", "number,headRefName,title"))
    packs = []
    # mtime-sorted so the last entry is the most recently previewed pack
    for f in sorted((DATA / "dist").glob("*.json"), key=lambda p: p.stat().st_mtime):
        try:
            d = json.loads(f.read_text())
            packs.append({"slug": d["slug"], "status": d.get("status", "pending")})
        except Exception:
            continue
    cands = []
    if date:
        try:
            cands = json.loads((DATA / f"selection-{date}.json").read_text()).get(
                "deep_dive_candidates", [])
        except Exception:
            pass
    ctx = {
        "open_prs": open_prs,
        "distribution_packs": packs,
        "deep_dive_candidates": [{"rank": c.get("rank"), "title": c.get("title")} for c in cands],
    }
    router_prompt = (
        "你是内容管线的指令路由器。用户在 Discord 发了一条消息，判断意图并输出严格 JSON（不要其他文字）：\n"
        '{"action": "revise_article" | "revise_distribution" | "schedule" | "select_topics" | "new_topic" | "none",\n'
        ' "slug": "<相关文章 slug，或空>", "lang_suffix": "-en 或空（改英文版文章时用）",\n'
        ' "ranks": [<select_topics 时的编号>], "feedback": "<用户的修改意见原文>",\n'
        ' "topic": "<new_topic 时：用户想写的话题描述原文，链接原样保留>"}\n\n'
        "判断依据：\n"
        "- 提到 thread/推文/LinkedIn 帖/预览/分发内容 的修改意见 → revise_distribution\n"
        "- 对博客文章本身的修改意见 → revise_article（明确说英文版时 lang_suffix=-en）\n"
        "- 表达「可以发了/排程吧/确认发布」→ schedule\n"
        "- 挑选题（提到编号或候选标题）→ select_topics\n"
        "- 提出候选清单之外的新话题想写成深度文章（描述一条新闻/论文/贴个链接说想写这个，"
        "或说候选都不喜欢想写别的）→ new_topic，topic 填用户描述原文\n"
        "- 闲聊、提问、与上述无关 → none\n"
        "- slug 从上下文推断：只有一个候选对象时直接用它\n"
        "- revise_distribution 的 slug 只能取 distribution_packs 里已有的 slug"
        "（列表按时间排序，最后一个=最新预览）；用户没点名文章时 slug 留空\n\n"
        f"## 当前上下文\n{json.dumps(ctx, ensure_ascii=False)}\n\n## 用户消息\n{content}"
    )
    run = subprocess.run(
        ["claude", "-p", "--output-format", "text", "--model", "sonnet"],
        input=router_prompt, cwd=REPO_ROOT, capture_output=True, text=True, timeout=120,
    )
    if run.returncode != 0:
        return False
    try:
        clean = subprocess.run(
            [sys.executable, str(SCRIPTS / "split_output.py"), "json"],
            input=run.stdout, capture_output=True, text=True, check=True,
        ).stdout
        intent = json.loads(clean)
    except Exception:
        return False
    action = intent.get("action")
    slug = (intent.get("slug") or "").strip()
    feedback = (intent.get("feedback") or content).strip()
    if action == "none":
        return True  # deliberate chatter, stay silent
    if action == "revise_distribution":
        # Hard-validate against real packs: the router must never send
        # distribute.py after a slug with no pack (unpublished article etc.).
        pendings = [p["slug"] for p in packs if p["status"] != "scheduled"]
        if slug not in pendings:
            if len(pendings) == 1:
                slug = pendings[0]
            elif len(pendings) > 1:
                ask_which_pack(pendings, "改发 <slug> 意见")
                return True
            else:
                slug = ""
        if not slug:
            send("⚠️ 没有待发布的分发内容可改（都已排程或尚未生成）。")
            return True
    if action == "revise_distribution" and slug:
        send(f"✏️ 收到对 {slug} 分发内容的意见，重新生成中…")
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "distribute.py"), slug, feedback],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=1200,
        )
        if r.returncode != 0:
            send(f"⚠️ 分发内容重生成失败：\n```{(r.stderr or r.stdout)[-400:]}```")
    elif action == "revise_article" and slug:
        handle_revision(slug + (intent.get("lang_suffix") or ""), feedback)
    elif action == "schedule" and slug:
        handle_distribution(slug)
    elif action == "select_topics" and intent.get("ranks") and date:
        handle_selection(sorted(set(int(r) for r in intent["ranks"])), date)
    elif action == "new_topic" and (intent.get("topic") or "").strip():
        handle_new_topic(intent["topic"].strip())
    else:
        return False
    return True


def _finalize(state):
    STATE_FILE.write_text(json.dumps(state))
    print(f"[{datetime.now(timezone.utc).isoformat()}] processed up to {state['last_id']}")


if __name__ == "__main__":
    main()
