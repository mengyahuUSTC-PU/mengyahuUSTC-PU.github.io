#!/usr/bin/env python3
"""Poll open bot-created PRs (post/*, fix/*) for new user comments and treat
each as revision feedback: revise the article on that PR's branch and push.

First run baselines existing comments (no action). State:
automation/data/state/pr_comments.json  {"seen": [comment ids]}
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "automation" / "data"
STATE_FILE = DATA / "state" / "pr_comments.json"
SCRIPTS = REPO_ROOT / "automation" / "scripts"
PROMPTS = REPO_ROOT / "automation" / "prompts"

BOT_MARKERS = ("Generated with [Claude Code]", "已按此条评论修改")

sys.path.insert(0, str(SCRIPTS))
from discord_notify import load_env, send  # noqa: E402


def sh(*cmd, timeout=300):
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=timeout
    ).stdout.strip()


def article_path(pr_number: int) -> str | None:
    files = json.loads(sh("gh", "pr", "view", str(pr_number), "--json", "files"))["files"]
    for f in files:
        if re.match(r"src/content/blog/(zh|en)/.+\.md$", f["path"]):
            return f["path"]
    return None


def revise(pr_number: int, branch: str, rel: str, feedback: str) -> bool:
    baseline = (PROMPTS / "editorial-baseline.md").read_text()
    lessons = (PROMPTS / "editorial-lessons.md").read_text()
    revise_p = (PROMPTS / "revise.md").read_text()
    sh("git", "fetch", "-q", "origin")
    sh("git", "checkout", "-q", "-B", branch, f"origin/{branch}")
    article = (REPO_ROOT / rel).read_text()
    prompt = (
        baseline
        + "\n\n" + lessons
        + "\n\n" + revise_p
        + "\n\n注意：提问视为行动请求（问「有没有没做完的」= 把它做完）。"
          "仅当意见完全没有可执行含义（如单纯认可「LGTM」）时才原样返回文件全文。"
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
        raise RuntimeError((run.stderr or run.stdout)[-400:])
    clean = subprocess.run(
        [sys.executable, str(SCRIPTS / "split_output.py"), "json"],
        input=run.stdout, capture_output=True, text=True, check=True,
    ).stdout
    if not clean.strip().startswith("---") or clean.strip() == article.strip():
        sh("git", "checkout", "-q", "master")
        return False
    if sh("git", "rev-parse", "--abbrev-ref", "HEAD") != branch:
        raise RuntimeError(f"refusing to commit: not on {branch}")
    (REPO_ROOT / rel).write_text(clean)
    sh("git", "add", rel)
    sh("git", "commit", "-q", "-m",
       f"Revise per PR #{pr_number} comment\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>")
    sh("git", "push", "-q", "origin", branch)
    try:
        from sync_pair import sync_counterpart
        if sync_counterpart(branch, rel):
            send("🔁 另一语言版本已同步同样的修改。")
    except Exception as exc:
        send(f"⚠️ 双语同步失败（需人工检查另一版）：{str(exc)[:200]}")
    sh("git", "checkout", "-q", "master")
    return True


def main():
    load_env()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    first_run = not STATE_FILE.exists()
    state = json.loads(STATE_FILE.read_text()) if not first_run else {"seen": []}
    seen = set(state["seen"])

    prs = json.loads(sh("gh", "pr", "list", "--state", "open",
                        "--json", "number,headRefName"))
    for pr in prs:
        branch = pr["headRefName"]
        if not (branch.startswith("post/") or branch.startswith("fix/")):
            continue
        number = pr["number"]
        # Conversation-tab comments (issues API)...
        comments = json.loads(sh(
            "gh", "api", f"repos/{{owner}}/{{repo}}/issues/{number}/comments",
            "--jq", "[.[] | {id, body, login: .user.login}]"
        ) or "[]")
        # ...plus inline review comments (pulls API) — these carry file/line
        # anchors, so the revision knows exactly what the comment refers to.
        inline = json.loads(sh(
            "gh", "api", f"repos/{{owner}}/{{repo}}/pulls/{number}/comments",
            "--jq", "[.[] | {id, body, path, line: (.line // .original_line), "
                    "hunk: .diff_hunk, login: .user.login}]"
        ) or "[]")

        feedback_parts = []
        inline_ids = []
        for c in comments:
            if c["id"] in seen:
                continue
            seen.add(c["id"])
            if first_run or any(m in c["body"] for m in BOT_MARKERS):
                continue
            feedback_parts.append(c["body"])
        for c in inline:
            key = f"r{c['id']}"
            if key in seen:
                continue
            seen.add(key)
            if first_run or any(m in c["body"] for m in BOT_MARKERS):
                continue
            inline_ids.append(c["id"])
            context = (c.get("hunk") or "").splitlines()[-3:]
            feedback_parts.append(
                f"【inline 定位：{c.get('path')} 第 {c.get('line')} 行，评论所指的原文片段：】\n"
                + "\n".join("> " + l.lstrip("+- ") for l in context)
                + f"\n意见：{c['body']}"
            )

        if feedback_parts:
            rel = article_path(number)
            if not rel:
                continue
            combined = "\n\n---\n\n".join(feedback_parts)
            send(f"✏️ 收到 PR #{number} 里的 {len(feedback_parts)} 条评论（含 inline 定位），按它们改稿中…")
            try:
                changed = revise(number, branch, rel, combined)
            except Exception as exc:
                send(f"⚠️ PR #{number} 评论改稿失败：\n```{str(exc)[-400:]}```")
                continue
            c = {"body": combined}
            if changed:
                try:
                    from editorial_memory import update_lessons
                    from datetime import datetime, timezone
                    update_lessons(c["body"], datetime.now(timezone.utc).strftime("%Y-%m-%d"))
                except Exception:
                    pass
                sh("gh", "pr", "comment", str(number), "--body",
                   "已按上面的评论修改，见最新 commit。\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)")
                # Reply inside each inline thread so it doesn't look unanswered.
                for cid in inline_ids:
                    try:
                        sh("gh", "api", "-X", "POST",
                           f"repos/{{owner}}/{{repo}}/pulls/{number}/comments/{cid}/replies",
                           "-f", "body=已按此条评论修改，见最新 commit。\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)")
                    except Exception:
                        pass
                send(f"✅ PR #{number} 已按评论更新（inline 线程已逐条回复），刷新即可复审。")
            else:
                send(f"ℹ️ PR #{number} 的评论未包含实质修改要求，文章未改动。")

    state["seen"] = sorted(seen, key=str)
    STATE_FILE.write_text(json.dumps(state))


if __name__ == "__main__":
    main()
