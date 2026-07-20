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


def handle_distribution(slug: str):
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

    # User decision (2026-07-19): publish immediately on approval — freshness
    # over optimal-hour scheduling.
    try:
        create_draft(thread=[pack["thread"].strip()], publish_at="now", title=f"{slug} (X)")
        create_draft(linkedin=pack["linkedin"], publish_at="now",
                     title=f"{slug} (LinkedIn)")
    except Exception as exc:
        send(f"⚠️ Typefully 发布失败（{slug}）：{str(exc)[:300]}")
        return

    pack["status"] = "scheduled"
    pack["scheduled_for"] = {"x": "now", "linkedin": "now",
                             "at": datetime.now(timezone.utc).isoformat()}
    dist_file.write_text(json.dumps(pack, ensure_ascii=False, indent=2))
    send(f"🚀 {slug} 的 X 帖 + LinkedIn 帖已提交立即发布（Typefully 处理中，1-2 分钟内上线）。")


HELP_TEXT = ("🤔 没听懂。可用指令：\n"
             "`1 3` 选题 · `改文章 [slug] 意见` · `改简报 意见` · "
             "`改L 意见`（LinkedIn）· `改X 意见`（thread）· `发 [slug]` 排程")


def latest_briefing_slug():
    posts = sorted((REPO_ROOT / "src" / "content" / "blog" / "zh").glob("briefing-*.md"))
    return posts[-1].stem if posts else None


def latest_article_slug():
    posts = [p for p in (REPO_ROOT / "src" / "content" / "blog" / "zh").glob("*.md")
             if not p.stem.startswith("briefing-") and p.stem != "hello-world"]
    if not posts:
        return None
    return max(posts, key=lambda p: p.stat().st_mtime).stem


def handle_dist_edit(part: str, feedback: str):
    """Revise only one part (thread/linkedin) of the newest pending dist pack."""
    packs = sorted((DATA / "dist").glob("*.json"), key=lambda p: p.stat().st_mtime)
    if not packs:
        send("⚠️ 没有待发布的分发内容。")
        return
    pack = json.loads(packs[-1].read_text())
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
            slug_ = next((s for s in pending if s in tokens), None) or (pending[-1] if pending else None)
            if slug_:
                handle_distribution(slug_)
            else:
                send("ℹ️ 没有待排程的分发内容（都已排程或尚未生成）。")
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
                send(f"📬 选题 {rank} 草稿已开 PR：{pr}\n手机上 Merge = 发布；要改就在 PR 留言。独立核查随后跟进…")
                m = re.search(r"/pull/(\d+)", pr)
                if m:
                    subprocess.run(
                        [sys.executable, str(SCRIPTS / "verify_draft.py"), m.group(1)],
                        cwd=REPO_ROOT, capture_output=True, text=True, timeout=1200,
                    )
            except subprocess.CalledProcessError as exc:
                send(f"⚠️ 选题 {rank} 写稿失败：\n```{(exc.stderr or str(exc))[-500:]}```")


def route_free_text(content, date):
    """Classify a free-form message and dispatch. Silent on unrelated chatter."""
    open_prs = json.loads(sh("gh", "pr", "list", "--state", "open",
                             "--json", "number,headRefName,title"))
    packs = []
    for f in (DATA / "dist").glob("*.json"):
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
        '{"action": "revise_article" | "revise_distribution" | "schedule" | "select_topics" | "none",\n'
        ' "slug": "<相关文章 slug，或空>", "lang_suffix": "-en 或空（改英文版文章时用）",\n'
        ' "ranks": [<select_topics 时的编号>], "feedback": "<用户的修改意见原文>"}\n\n'
        "判断依据：\n"
        "- 提到 thread/推文/LinkedIn 帖/预览/分发内容 的修改意见 → revise_distribution\n"
        "- 对博客文章本身的修改意见 → revise_article（明确说英文版时 lang_suffix=-en）\n"
        "- 表达「可以发了/排程吧/确认发布」→ schedule\n"
        "- 挑选题（提到编号或候选标题）→ select_topics\n"
        "- 闲聊、提问、与上述无关 → none\n"
        "- slug 从上下文推断：只有一个候选对象时直接用它\n\n"
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
    else:
        return False
    return True


def _finalize(state):
    STATE_FILE.write_text(json.dumps(state))
    print(f"[{datetime.now(timezone.utc).isoformat()}] processed up to {state['last_id']}")


if __name__ == "__main__":
    main()
