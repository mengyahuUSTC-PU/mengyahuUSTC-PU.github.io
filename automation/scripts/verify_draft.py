#!/usr/bin/env python3
"""Independent fact-check + auto-fix pass over a PR's article(s).

Usage: verify_draft.py <pr_number>

1. GPT, through the Codex CLI on the owner's ChatGPT plan, checks every
   claim: cited? source supports it? For uncited claims it searches the web
   for a suitable source and records it. Until 2026-10-20 Opus and Fable
   checked as well; that was half of the pipeline's Claude use, and the owner
   chose to let GPT carry it alone. When GPT cannot run (login, usage limit),
   Opus takes its place, so no article goes unchecked.
2. If the verifier flags issues, GPT returns a list of sentence-level edits
   (exact original text -> replacement) and this script applies the ones
   that match exactly once, so the rest of the article stays as written.
   Claude rewrites the article only when GPT cannot run. Revised on the
   PR branch: adds the found citations, downgrades/removes anything
   unverifiable or contradicted. One fix iteration, then human review.
3. Full reports + an auto-fix summary are posted as a PR comment.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLAUDE = "/home/mia/bin/claude-pipe"  # tools, MCP and usage limits: see automation/scripts/claude-pipe
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

**不要核查作者的判断。** 观点、评价、趋势推断、对意义的解读（例如「这说明……」「值得注意的是……」、
每段结尾的点评、「今日一句话」）是作者的分析，不是事实断言，不进表格；
只有当这类句子里夹着可核实的具体事实（数字、日期、谁做了什么）时，才把那个事实单独拿出来核查。

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
        [CLAUDE, "-p", "--output-format", "text", "--model", model,
         "--allowedTools", "WebFetch", "WebSearch"],
        input=VERIFY_PROMPT + "\n\n## 待核查文章\n\n" + content,
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=900,
    )
    return run.stdout.strip() if run.returncode == 0 else None


# The owner's ChatGPT Pro plan (humengyahumy, since 2026-10-20) through Codex.
# GPT-6 Astra is its strongest model; reasoning is set explicitly because
# Codex 0.163 defaults to none, and stdin is closed because exec now appends
# whatever stdin carries to the prompt.
GPT_MODEL = "gpt-6-astra"
GPT_EFFORT = "high"


def codex(prompt: str, out_path: str, schema: str | None = None) -> subprocess.CompletedProcess:
    cmd = ["codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check",
           "-m", GPT_MODEL, "-c", f'model_reasoning_effort="{GPT_EFFORT}"',
           "--output-last-message", out_path]
    if schema:
        cmd += ["--output-schema", schema]
    return subprocess.run(cmd + [prompt], cwd=REPO_ROOT, capture_output=True, text=True,
                          timeout=900, stdin=subprocess.DEVNULL)


def gpt_verify(content: str) -> str:
    """Cross-vendor check via the OpenAI Codex CLI."""
    import shutil

    if not shutil.which("codex"):
        return "⚠️ codex CLI 未安装，跳过 GPT 核查。"
    import tempfile

    with tempfile.NamedTemporaryFile(mode="r", suffix=".md") as out:
        run = codex(VERIFY_PROMPT + "\n\n## 待核查文章\n\n" + content, out.name)
        if run.returncode != 0:
            err = (run.stderr or run.stdout)[-200:]
            if "login" in err.lower() or "auth" in err.lower():
                return "⚠️ codex 未登录（需要用户完成 ChatGPT 授权），跳过 GPT 核查。"
            return f"⚠️ GPT 核查失败：{err}"
        result = out.read().strip()
    return result or "⚠️ GPT 返回为空。"


FLAG_MARKS = ("🔗", "⚠️", "❌", "🚫")

def _assert_on(branch: str):
    cur = sh("git", "rev-parse", "--abbrev-ref", "HEAD")
    if cur != branch:
        raise RuntimeError(f"refusing to commit: on '{cur}', expected '{branch}'")



GPT_FIX_PROMPT = """你是这篇文章的编辑。核查员对文章提交了下面的报告。请给出最小的逐句修改清单：

- 只处理报告里标为 🔗 / ⚠️ / ❌ / 🚫 的条目；✅ 的条目和报告没点名的句子一律不动，不要顺手润色
- 🔗 缺引用已找到来源：在对应断言处补上 Markdown 内联链接 [文字](URL)，只用报告里给出、且你核实过确实支持该断言的链接
- ⚠️ 来源不符：以来源原文为准改正说法
- ❌ 查无来源：删除，或改写成明确标出不确定的说法
- 🚫 与事实矛盾：改正或删除
- 作者的判断、观点、趋势推断和结尾点评保持原样。报告如果把这类句子当成事实标了出来，跳过这一条；只有句子里夹着被证伪的具体事实时，才只改那个事实，判断本身留着
- 改后的句子要像作者原文：保持原文的语言（中文就写中文）、语气和标点习惯，遵守附在后面的编辑方针，不要加入新的修辞

输出 edits 数组。每一项：find 是文章里要改的原文，逐字复制、不改一个字符，只取够唯一定位的最短片段（通常是一句）；replace 是替换后的文字（删除时为空字符串）；why 用一句话说明对应报告的哪一条。没有需要改的就输出空数组。
"""

GPT_FIX_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["edits"],
    "properties": {"edits": {"type": "array", "items": {
        "type": "object", "additionalProperties": False, "required": ["find", "replace", "why"],
        "properties": {"find": {"type": "string"}, "replace": {"type": "string"}, "why": {"type": "string"}}}}},
}


def gpt_edits(article: str, reports: list[str], baseline: str, lessons: str) -> list[dict] | None:
    """Sentence-level fixes from GPT; None when GPT could not run."""
    import shutil
    import tempfile

    if not shutil.which("codex"):
        return None
    prompt = (GPT_FIX_PROMPT + "\n\n## 核查报告\n\n" + "\n\n---\n\n".join(reports)
              + "\n\n## 编辑方针\n\n" + baseline + "\n\n" + lessons
              + "\n\n## 文章当前版本\n\n" + article)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as schema, \
            tempfile.NamedTemporaryFile(mode="r", suffix=".json") as out:
        json.dump(GPT_FIX_SCHEMA, schema)
        schema.flush()
        run = codex(prompt, out.name, schema=schema.name)
        if run.returncode != 0:
            return None
        try:
            return json.loads(out.read()).get("edits", [])
        except ValueError:
            return None


def apply_edits(article: str, edits: list[dict]) -> tuple[str, list[str], list[str]]:
    """Apply edits whose `find` occurs exactly once in the body. Frontmatter is
    never touched; an edit that does not match exactly is skipped, not guessed."""
    head, sep, body = article.partition("\n---\n")
    if not article.startswith("---") or not sep:
        return article, [], [e.get("why", "") for e in edits]
    applied, skipped = [], []
    for e in edits:
        find, repl = e.get("find", ""), e.get("replace", "")
        if find and body.count(find) == 1:
            body = body.replace(find, repl)
            applied.append(e.get("why", ""))
        else:
            skipped.append(e.get("why", "") or find[:40])
    return head + sep + body, applied, skipped


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

    edits = gpt_edits(article, reports, baseline, lessons)
    if edits is not None:
        new, applied, skipped = apply_edits(article, edits)
        ok = False
        # A fix pass adds citations and softens claims; losing a third of the
        # text means something went wrong, so keep the article as it was.
        if applied and new != article and len(new) > 0.7 * len(article):
            _assert_on(branch)
            (REPO_ROOT / rel).write_text(new)
            sh("git", "add", rel)
            sh("git", "commit", "-q", "-m",
               f"Apply fact-check findings: {len(applied)} sentence-level edits by {GPT_MODEL}\n\n"
               + "\n".join(f"- {w}" for w in applied)
               + (f"\n\nSkipped (no exact match): {len(skipped)}" if skipped else ""))
            sh("git", "push", "-q", "origin", branch)
            try:
                from sync_pair import sync_counterpart
                sync_counterpart(branch, rel)
            except Exception:
                pass
            ok = True
        if skipped:
            send(f"ℹ️ {rel}：GPT 给的 {len(skipped)} 处修改没找到唯一匹配的原文，已跳过，详见 PR 评论里的核查报告。")
        sh("git", "checkout", "-q", "master")
        return ok

    # GPT could not run: Claude rewrites the article as before.
    prompt = (
        baseline
        + "\n\n" + lessons
        + "\n\n" + FIX_PROMPT
        + "\n\n## 核查员报告\n\n" + "\n\n---\n\n".join(reports)
        + "\n\n## 文章当前版本\n\n" + article
    )
    run = subprocess.run(
        [CLAUDE, "-p", "--output-format", "text",
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

    all_reports, fixed_files, unchecked, all_checked = [], [], [], []
    for rel in md_files:
        content = sh("git", "show", f"{src_ref}:{rel}")
        file_reports, checked = [], []
        gpt = gpt_verify(content)
        if gpt.startswith("⚠️"):  # GPT did not run; its error is not a finding
            out = claude_verify(content, "opus")
            file_reports.append(f"### `{rel}` · 核查员 Opus 5.5（GPT 未能运行：{gpt[2:].strip()[:120]}）"
                                f"\n\n{out or '⚠️ 核查器运行失败'}")
            if out:
                checked.append(out)
            else:
                unchecked.append(rel)
        else:
            file_reports.append(f"### `{rel}` · 核查员 GPT（经 Codex CLI）\n\n{gpt}")
            checked.append(gpt)
        all_reports.extend(file_reports)
        all_checked.extend(checked)

        if any(any(m in r for m in FLAG_MARKS) for r in checked):
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
                        "--body", f"核查对已合并的 #{pr} 的修正。Merge = 修正上线。\n\n"
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
        + f"\n\n*核查：{GPT_MODEL}（经 Codex CLI，用 ChatGPT 会员额度），GPT 无法运行时由 Opus 5.5 代替；"
          "缺引用的断言由核查员找源，GPT 按报告逐句修改（只动被点名的句子），无法核实的自动降级。*"
        + "\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)"
    )
    sh("gh", "pr", "comment", pr, "--body", body)
    flags = sum(r.count(m) for r in all_checked for m in FLAG_MARKS)  # findings, not run errors
    icon = "🟢" if flags == 0 else "🟡"
    fixed_note = f"，其中 {len(fixed_files)} 个文件已自动修正" if fixed_files else ""
    if unchecked:
        send(f"🚨 PR #{pr} 有文件没能核查（GPT 和 Opus 都没跑成）：{', '.join(unchecked)}")
    if all_checked:
        send(f"{icon} PR #{pr} 核查完成：{'全部断言核实通过' if flags == 0 else f'{flags} 处被标记{fixed_note}'}，详见 PR 评论。")
    print(f"verified PR #{pr}: {flags} flags, fixed: {fixed_files}")


if __name__ == "__main__":
    main()
