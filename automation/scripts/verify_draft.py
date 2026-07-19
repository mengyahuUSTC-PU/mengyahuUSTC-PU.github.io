#!/usr/bin/env python3
"""Independent fact-check pass over a PR's article(s).

Usage: verify_draft.py <pr_number>

Runs AFTER a PR is created: a fresh-context model (different from the
writer) re-fetches every cited source and checks each factual claim, then
posts the verdict table as a PR comment. Verification never blocks the PR —
it adds information for the human reviewer.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "automation" / "scripts"

sys.path.insert(0, str(SCRIPTS))
from discord_notify import load_env, send  # noqa: E402

VERIFY_PROMPT = """你是独立事实核查员，与文章作者无关。你会收到一篇待发布的博客文章。

任务：
1. 列出文中每一个**事实性断言**（数字、日期、事件、引语、「X 没有做 Y」类否定断言）
2. 用 WebFetch 打开文中引用的来源逐条核对；断言没挂引用的，用 WebSearch 找权威来源核对
3. 特别警惕：文中数字与来源不一致、来源根本不支持该断言、断言无任何来源可查

输出格式（严格遵守，不要其他内容）：

## 独立核查报告

| 断言 | 判定 | 依据 |
|---|---|---|
| <断言摘要> | ✅核实 / ⚠️来源不符 / ❌查无来源 | <一句话+链接> |

**结论**：<一句话——可放心发布 / 有 N 处需人工复核（列出）>
"""


def sh(*cmd, timeout=300):
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=timeout
    ).stdout.strip()


def main():
    pr = sys.argv[1]
    load_env()
    files = json.loads(sh("gh", "pr", "view", pr, "--json", "files"))["files"]
    md_files = [f["path"] for f in files
                if re.match(r"src/content/blog/(zh|en)/.+\.md$", f["path"])]
    if not md_files:
        print("no article files in PR")
        return

    branch = json.loads(sh("gh", "pr", "view", pr, "--json", "headRefName"))["headRefName"]
    sh("git", "fetch", "-q", "origin")

    VERIFIERS = [("opus", "Opus 4.8"), ("fable", "Fable 5")]
    reports = []
    for rel in md_files:
        content = sh("git", "show", f"origin/{branch}:{rel}")
        for model, label in VERIFIERS:
            run = subprocess.run(
                ["claude", "-p", "--output-format", "text",
                 "--model", model,
                 "--allowedTools", "WebFetch", "WebSearch"],
                input=VERIFY_PROMPT + "\n\n## 待核查文章\n\n" + content,
                cwd=REPO_ROOT, capture_output=True, text=True, timeout=900,
            )
            if run.returncode != 0:
                reports.append(f"### `{rel}` · 核查员 {label}\n\n⚠️ 核查器运行失败：{(run.stderr or run.stdout)[-200:]}")
            else:
                reports.append(f"### `{rel}` · 核查员 {label}\n\n{run.stdout.strip()}")

    body = (
        "\n\n".join(reports)
        + "\n\n*双核查：Opus 4.8 与 Fable 5 各自独立上下文（与写作会话分离），逐条重访来源。*"
        + "\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)"
    )
    sh("gh", "pr", "comment", pr, "--body", body)
    flagged = body.count("⚠️") + body.count("❌")
    icon = "🟢" if flagged == 0 else "🟡"
    send(f"{icon} PR #{pr} 独立核查完成：{'全部断言核实通过' if flagged == 0 else f'{flagged} 处需人工复核'}，详见 PR 评论。")
    print(f"verified PR #{pr}: {flagged} flags")


if __name__ == "__main__":
    main()
