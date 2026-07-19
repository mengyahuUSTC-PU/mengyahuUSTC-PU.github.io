#!/usr/bin/env python3
"""Long-term editorial memory: distill each piece of user feedback into a
generalizable lesson appended to automation/prompts/editorial-lessons.md,
then commit the update to master.

Called by the revision handlers after acting on feedback. Failures are
non-fatal (a missed lesson never blocks the revision itself).
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LESSONS = REPO_ROOT / "automation" / "prompts" / "editorial-lessons.md"

DISTILL_PROMPT = """你维护一份「编辑教训」文件：作者对 AI 写作的历次反馈提炼成的通用规则。

下面是文件当前内容，以及作者刚给出的一条新反馈。你的任务：
1. 判断这条反馈里是否含有**可泛化到未来文章**的偏好或规则（针对单篇具体内容的意见不算）
2. 若有：把它并入文件——放进合适的分组（必要时新建分组），与既有规则合并去重，一条规则一行，末尾注明日期；保持全文精炼（不超过 40 条规则）
3. 若没有可泛化内容：原样返回文件

**只输出更新后的文件全文**，不要解说。
"""


def update_lessons(feedback: str, date: str) -> bool:
    current = LESSONS.read_text() if LESSONS.exists() else "# 编辑教训\n"
    prompt = (
        DISTILL_PROMPT
        + f"\n\n## 文件当前内容\n\n{current}"
        + f"\n\n## 新反馈（{date}）\n\n{feedback}"
    )
    run = subprocess.run(
        ["claude", "-p", "--output-format", "text"],
        input=prompt, cwd=REPO_ROOT, capture_output=True, text=True, timeout=300,
    )
    if run.returncode != 0:
        return False
    new = run.stdout.strip()
    if not new.startswith("#") or new == current.strip():
        return False
    try:
        subprocess.run(["git", "stash", "-q", "--include-untracked"],
                       cwd=REPO_ROOT, check=False, capture_output=True)
        subprocess.run(["git", "checkout", "-q", "master"], cwd=REPO_ROOT,
                       check=True, capture_output=True)
        subprocess.run(["git", "pull", "-q", "origin", "master"], cwd=REPO_ROOT,
                       check=True, capture_output=True)
        LESSONS.write_text(new + "\n")
        subprocess.run(["git", "add", str(LESSONS)], cwd=REPO_ROOT,
                       check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-q", "-m",
             "Update editorial lessons from user feedback\n\n"
             "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"],
            cwd=REPO_ROOT, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "-q", "origin", "master"], cwd=REPO_ROOT,
                       check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    ok = update_lessons(sys.stdin.read(), sys.argv[1] if len(sys.argv) > 1 else "")
    print("updated" if ok else "no change")
