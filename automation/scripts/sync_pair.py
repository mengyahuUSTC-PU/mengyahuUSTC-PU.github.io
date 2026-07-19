#!/usr/bin/env python3
"""Keep zh/en article pairs aligned after automated edits.

sync_counterpart(branch, rel): treat the just-edited file as reference and
merge its substantive changes into the counterpart language file on the same
branch (native rewrite, merge semantics — never dropping the counterpart's
own existing corrections). Commits and pushes if anything changed.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "automation" / "scripts"
PROMPTS = REPO_ROOT / "automation" / "prompts"

SYNC_PROMPT = """博客文章有中英两个版本，内容必须保持实质对称。下面给出：
1. **参照版**：刚被修改过的版本（其中的修正是权威的）
2. **目标版**：另一语言的当前版本

任务：把参照版中存在、而目标版缺失的**实质性修正**（事实更正、新增/替换的引用、删除的不实断言、措辞降级）合并进目标版。

规则：
- **删除也是修正**：参照版里被删掉的段落/条目（目标版仍有对应内容），目标版必须同步删除，并连带修顺受影响的标题/总结句
- 用目标版语言的**原生行文**表达，不逐句翻译
- **合并语义**：只补缺失的修正；目标版已有的其他内容和它自己的修正一律保留
- 与修正无关的部分一个字不动
- frontmatter 不动（各自语言的 title/description 保持原样，除非参照版的修正涉及标题事实错误）
- 若目标版已包含全部实质修正，**原样返回目标版全文**

**最终回复只包含目标版文件全文**（含 frontmatter），不要解说。
"""


def sh(*cmd, timeout=300):
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=timeout
    ).stdout.strip()


def counterpart_of(rel: str) -> str | None:
    if "/zh/" in rel:
        return rel.replace("/zh/", "/en/")
    if "/en/" in rel:
        return rel.replace("/en/", "/zh/")
    return None


def sync_counterpart(branch: str, rel: str) -> bool:
    """Assumes the branch is already checked out with `rel` at its new state.
    Returns True if the counterpart was updated (committed + pushed)."""
    other = counterpart_of(rel)
    if not other or not (REPO_ROOT / other).exists():
        return False

    reference = (REPO_ROOT / rel).read_text()
    target = (REPO_ROOT / other).read_text()
    prompt = (
        SYNC_PROMPT
        + "\n\n## 参照版（权威）\n\n" + reference
        + "\n\n## 目标版（待同步）\n\n" + target
    )
    run = subprocess.run(
        ["claude", "-p", "--output-format", "text",
         "--model", "fable", "--fallback-model", "opus"],
        input=prompt, cwd=REPO_ROOT, capture_output=True, text=True, timeout=900,
    )
    if run.returncode != 0:
        return False
    clean = subprocess.run(
        [sys.executable, str(SCRIPTS / "split_output.py"), "json"],
        input=run.stdout, capture_output=True, text=True, check=True,
    ).stdout
    if not clean.strip().startswith("---") or clean.strip() == target.strip():
        return False
    cur = sh("git", "rev-parse", "--abbrev-ref", "HEAD")
    if cur != branch:
        raise RuntimeError(f"sync refusing to commit: on '{cur}', expected '{branch}'")
    (REPO_ROOT / other).write_text(clean)
    sh("git", "add", other)
    sh("git", "commit", "-q", "-m",
       f"Sync counterpart language version ({Path(other).parts[-2]})\n\n"
       "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>")
    sh("git", "push", "-q", "origin", branch)
    return True


if __name__ == "__main__":
    print(sync_counterpart(sys.argv[1], sys.argv[2]))
