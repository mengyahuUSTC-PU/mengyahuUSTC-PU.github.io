#!/usr/bin/env python3
"""Audit channel entrypoint. Runs inside the dedicated audit clone
(/home/mia/site-audit) so long audits never block the main pipeline lock.

Usage: audit_and_continue.py <pr_number> <slug>
Runs the three-model audit, then the follow-up: fix-PR notice, or EN
generation when the audit is clean.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "automation" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from discord_notify import load_env, send  # noqa: E402
from poll_merged import generate_en, sh  # noqa: E402


def main():
    pr, slug = sys.argv[1], sys.argv[2]
    load_env()
    run = subprocess.run(
        [sys.executable, str(SCRIPTS / "verify_draft.py"), pr],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=2400,
    )
    if run.returncode != 0:
        send(f"⚠️ 三方核查运行失败（PR #{pr}）：\n```{(run.stderr or run.stdout)[-400:]}```")
        return
    open_fix = sh("gh", "pr", "list", "--state", "open",
                  "--head", f"fix/pr{pr}-factcheck", "--json", "number").strip()
    if json.loads(open_fix or "[]"):
        send("核查发现问题，修正 PR 已开（见上方链接）。**Merge 修正后我再生成英文版。**")
    else:
        sh("git", "fetch", "-q", "origin")
        sh("git", "checkout", "-q", "-B", "master", "origin/master")
        generate_en(slug)


if __name__ == "__main__":
    main()
