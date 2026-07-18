#!/usr/bin/env python3
"""Turn draft file(s) into a blog-post branch + GitHub PR.

Usage:
  make_pr.py DRAFT.md [DRAFT2.md ...]

Each draft is a complete markdown file with frontmatter (title, lang, slug…).
The trailing HTML comment block (fact-check list / alt titles), if present,
is stripped from the published file and moved into the PR body.

Requires: git identity + gh auth configured on this machine.
Prints the PR URL on success.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def sh(*cmd, **kw):
    return subprocess.run(cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True, **kw).stdout.strip()


def parse(draft_path: Path):
    text = draft_path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"error: {draft_path} has no frontmatter")
    fm_text, body = m.groups()
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip("\"'")
    comment = ""
    cm = re.search(r"<!--\n?(.*?)-->\s*$", body, re.S)
    if cm:
        comment = cm.group(1).strip()
        body = body[: cm.start()].rstrip() + "\n"
    return fm, f"---\n{fm_text}\n---\n{body}", comment


def main():
    drafts = [Path(p).resolve() for p in sys.argv[1:]]
    if not drafts:
        sys.exit(__doc__)

    parsed = [parse(p) for p in drafts]
    slug = parsed[0][0].get("slug") or drafts[0].stem
    lang = parsed[0][0].get("lang", "zh")
    branch = f"post/{slug}" if lang == "zh" else f"post/{slug}-{lang}"

    sh("git", "fetch", "-q", "origin", "master")
    sh("git", "checkout", "-q", "-B", branch, "origin/master")

    titles, comments = [], []
    for fm, content, comment in parsed:
        lang = fm.get("lang", "zh")
        dest = REPO_ROOT / "src" / "content" / "blog" / lang / f"{fm.get('slug', slug)}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
        sh("git", "add", str(dest))
        titles.append(f"[{lang}] {fm.get('title', slug)}")
        if comment:
            comments.append(comment)

    sh("git", "commit", "-q", "-m", f"Add post: {slug}\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>")
    sh("git", "push", "-q", "-f", "origin", branch)

    body_parts = [
        "## 摘要",
        parsed[0][0].get("description", "(无)"),
        "",
        "## 自查清单",
        "- [ ] 不含雇主内部信息，观点署名个人",
        "- [ ] 事实核查点已逐条核对（见下）",
        "- [ ] 语言风格符合编辑方针",
    ]
    if comments:
        body_parts += ["", "## 事实核查点 / 备选标题", *comments]
    body_parts += ["", "**Merge = 发布上线。** 需要修改请在 PR 里留言。", "", "🤖 Generated with [Claude Code](https://claude.com/claude-code)"]

    pr_url = sh(
        "gh", "pr", "create",
        "--title", titles[0],
        "--body", "\n".join(body_parts),
        "--base", "master",
        "--head", branch,
    )
    sh("git", "checkout", "-q", "master")
    print(pr_url)


if __name__ == "__main__":
    main()
