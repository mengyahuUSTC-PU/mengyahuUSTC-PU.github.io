#!/usr/bin/env python3
"""Independent fact-check + auto-fix pass over a PR's article(s).

Usage: verify_draft.py <pr_number>

1. Three independent verifiers (Opus 4.8, Fable 5, GPT via Codex CLI)
   check every claim: cited? source supports it? For uncited claims they
   search the web for a suitable source and record it.
2. If any verifier flags issues, the writer model revises the article on
   the PR branch: adds the found citations, downgrades/removes anything
   unverifiable or contradicted. One fix iteration, then human review.
3. Full reports + an auto-fix summary are posted as a PR comment.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "automation" / "scripts"
PROMPTS = REPO_ROOT / "automation" / "prompts"

sys.path.insert(0, str(SCRIPTS))
from discord_notify import load_env, send  # noqa: E402

VERIFY_PROMPT = """你是独立事实核查员，与文章作者无关。你会收到一篇待发布的博客文章。

任务，对文中每一个**事实性断言**（数字、日期、事件、引语、「X 没有做 Y」类否定断言）：
1. 检查它有没有挂引用（内联链接或文末参考来源）
2. 有引用的：用 WebFetch 打开来源，核对断言与原文是否一致
3. **没有引用的：用 WebSearch/WebFetch 上网找一个合适的权威来源**（优先官方一手），把链接写进报告
4. 找不到任何支持来源、或找到相反事实的：明确标出

输出格式（严格遵守，不要其他内容）：

## 独立核查报告

| 断言 | 判定 | 依据/建议引用 |
|---|---|---|
| <断言摘要> | ✅有引用且核实 / 🔗缺引用已找到来源 / ⚠️来源不符 / ❌查无来源 / 🚫与事实矛盾 | <一句话+链接> |

**结论**：<一句话>
"""

FIX_PROMPT = """你是文章作者。独立核查员对你的文章提交了以下报告。请按报告修改文章：

- 🔗缺引用已找到来源：把核查员找到的链接以内联引用补进对应断言处（先用 WebFetch 确认该来源确实支持断言）
- ⚠️来源不符：以来源原文为准修正断言
- ❌查无来源：按编辑方针降级（删除，或改写为明确标注的存疑表述）
- 🚫与事实矛盾：修正或删除
- ✅的条目一律不动；不要顺手改动未被报告点名的内容

**最终回复只包含修改后的文章文件全文**（含 frontmatter），不要解说。
"""


def sh(*cmd, timeout=300):
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=timeout
    ).stdout.strip()


def claude_verify(content: str, model: str) -> str | None:
    run = subprocess.run(
        ["claude", "-p", "--output-format", "text", "--model", model,
         "--allowedTools", "WebFetch", "WebSearch"],
        input=VERIFY_PROMPT + "\n\n## 待核查文章\n\n" + content,
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=900,
    )
    return run.stdout.strip() if run.returncode == 0 else None


def gpt_verify(content: str) -> str:
    """Cross-vendor check via OpenAI Codex CLI (ChatGPT Plus subscription)."""
    import shutil

    if not shutil.which("codex"):
        return "⚠️ codex CLI 未安装，跳过 GPT 核查。"
    run = subprocess.run(
        ["codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check",
         VERIFY_PROMPT + "\n\n## 待核查文章\n\n" + content],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=900,
    )
    if run.returncode != 0:
        err = (run.stderr or run.stdout)[-200:]
        if "login" in err.lower() or "auth" in err.lower():
            return "⚠️ codex 未登录（需要用户完成 ChatGPT 授权），跳过 GPT 核查。"
        return f"⚠️ GPT 核查失败：{err}"
    return run.stdout.strip() or "⚠️ GPT 返回为空。"


FLAG_MARKS = ("🔗", "⚠️", "❌", "🚫")

def _assert_on(branch: str):
    cur = sh("git", "rev-parse", "--abbrev-ref", "HEAD")
    if cur != branch:
        raise RuntimeError(f"refusing to commit: on '{cur}', expected '{branch}'")



def fix_article(branch: str, rel: str, reports: list[str], base: str | None = None) -> bool:
    """One writer-model pass applying verifier findings on a branch.
    base: start point for a NEW branch (e.g. origin/master for merged PRs);
    None means the branch already exists at origin."""
    # Read prompts from master BEFORE switching branches: older PR branches
    # may predate these files.
    baseline = (PROMPTS / "editorial-baseline.md").read_text()
    lessons = (PROMPTS / "editorial-lessons.md").read_text()
    sh("git", "fetch", "-q", "origin")
    sh("git", "checkout", "-q", "-B", branch, base or f"origin/{branch}")
    article = (REPO_ROOT / rel).read_text()
    prompt = (
        baseline
        + "\n\n" + lessons
        + "\n\n" + FIX_PROMPT
        + "\n\n## 核查员报告\n\n" + "\n\n---\n\n".join(reports)
        + "\n\n## 文章当前版本\n\n" + article
    )
    run = subprocess.run(
        ["claude", "-p", "--output-format", "text",
         "--model", "fable", "--fallback-model", "opus",
         "--allowedTools", "WebFetch", "WebSearch"],
        input=prompt, cwd=REPO_ROOT, capture_output=True, text=True, timeout=900,
    )
    ok = False
    if run.returncode == 0:
        clean = subprocess.run(
            [sys.executable, str(SCRIPTS / "split_output.py"), "json"],
            input=run.stdout, capture_output=True, text=True, check=True,
        ).stdout
        if clean.strip().startswith("---") and clean.strip() != article.strip():
            _assert_on(branch)
            (REPO_ROOT / rel).write_text(clean)
            sh("git", "add", rel)
            sh("git", "commit", "-q", "-m",
               "Apply fact-check findings: add citations, fix/downgrade flagged claims\n\n"
               "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>")
            sh("git", "push", "-q", "origin", branch)
            try:
                from sync_pair import sync_counterpart
                sync_counterpart(branch, rel)
            except Exception:
                pass
            ok = True
    sh("git", "checkout", "-q", "master")
    return ok


def main():
    pr = sys.argv[1]
    load_env()
    info = json.loads(sh("gh", "pr", "view", pr, "--json", "files,headRefName,state"))
    branch = info["headRefName"]
    report_only = info.get("state") != "OPEN"  # merged/closed: report, don't auto-fix
    md_files = [f["path"] for f in info["files"]
                if re.match(r"src/content/blog/(zh|en)/.+\.md$", f["path"])]
    if not md_files:
        print("no article files in PR")
        return

    sh("git", "fetch", "-q", "origin")
    # Merged PRs: the branch may be deleted; the content lives on master now.
    src_ref = "origin/master" if report_only else f"origin/{branch}"

    # zh/en pairs: verify the EN version only (sources are English); the fix
    # then propagates to zh via sync_counterpart. Standalone zh (deep dives
    # before the EN exists) is verified directly.
    en_slugs = {Path(f).stem for f in md_files if "/en/" in f}
    skipped_zh = [f for f in md_files if "/zh/" in f and Path(f).stem in en_slugs]
    md_files = [f for f in md_files if f not in skipped_zh]

    all_reports, fixed_files = [], []
    for rel in md_files:
        content = sh("git", "show", f"{src_ref}:{rel}")
        file_reports = []
        for model, label in [("opus", "Opus 4.8"), ("fable", "Fable 5")]:
            out = claude_verify(content, model)
            file_reports.append(
                f"### `{rel}` · 核查员 {label}\n\n{out or '⚠️ 核查器运行失败'}")
        file_reports.append(f"### `{rel}` · 核查员 GPT（跨厂商）\n\n{gpt_verify(content)}")
        all_reports.extend(file_reports)

        if any(any(m in r for m in FLAG_MARKS) for r in file_reports):
            if report_only:
                # PR already merged: fixes go to a dedicated fix branch/PR.
                fix_branch = f"fix/pr{pr}-factcheck"
                base = "origin/master" if not fixed_files else None
                if fix_article(fix_branch, rel, file_reports, base=base):
                    fixed_files.append(rel)
            elif fix_article(branch, rel, file_reports):
                fixed_files.append(rel)

    fix_pr_url = ""
    if report_only and fixed_files:
        fix_pr_url = sh("gh", "pr", "create", "--base", "master",
                        "--head", f"fix/pr{pr}-factcheck",
                        "--title", f"Fact-check fixes for merged PR #{pr}",
                        "--body", f"三方核查对已合并的 #{pr} 的修正。Merge = 修正上线。\n\n"
                                  "🤖 Generated with [Claude Code](https://claude.com/claude-code)")
    if skipped_zh:
        all_reports.append(
            "### 中文版\n\n未单独核查：以英文版核查为准（来源均为英文），"
            "修正通过双语同步机制传导到中文版。")
    summary = ("\n\n---\n\n## 自动修正\n\n"
               + ((f"原 PR 已合并，修正走新 PR：{fix_pr_url}（{', '.join(f'`{f}`' for f in fixed_files)}）"
                   if report_only else
                   f"已按报告修正并推送新 commit：{', '.join(f'`{f}`' for f in fixed_files)}。✅ 项未动；请复审修正处。")
                  if fixed_files else "无需修正或修正未产生变化。"))
    body = (
        "\n\n".join(all_reports) + summary
        + "\n\n*三方核查：Opus 4.8、Fable 5（各自独立上下文）+ GPT（跨厂商，经 Codex CLI）；"
          "缺引用的断言由核查员找源、写作模型补引，无法核实的自动降级。*"
        + "\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)"
    )
    sh("gh", "pr", "comment", pr, "--body", body)
    flags = sum(body.count(m) for m in FLAG_MARKS)
    icon = "🟢" if flags == 0 else "🟡"
    fixed_note = f"，其中 {len(fixed_files)} 个文件已自动修正" if fixed_files else ""
    send(f"{icon} PR #{pr} 三方核查完成：{'全部断言核实通过' if flags == 0 else f'{flags} 处被标记{fixed_note}'}，详见 PR 评论。")
    print(f"verified PR #{pr}: {flags} flags, fixed: {fixed_files}")


if __name__ == "__main__":
    main()
