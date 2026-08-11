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
    mode = sys.argv[3] if len(sys.argv) > 3 else "zh"
    load_env()
    run = subprocess.run(
        [sys.executable, str(SCRIPTS / "verify_draft.py"), pr],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=2400,
    )
    if run.returncode != 0:
        send(f"⚠️ 三方核查运行失败（PR #{pr}）：\n```{(run.stderr or run.stdout)[-400:]}```")
        return
    if mode == "en":
        # User decision 2026-08-11: the EN PR is verified (fixes pushed to its
        # branch by verify_draft) and merged without review. poll_merged then
        # generates the distribution pack — the user's remaining gate is 「发」.
        try:
            sh("gh", "pr", "merge", pr, "--merge")
            send(f"✅ 英文版已核查并自动上线（{slug}）。分发预览随后送达，回「发」才对外分发。")
        except Exception as exc:
            send(f"⚠️ 英文版 PR 自动合并失败（#{pr}），请手动 Merge：{str(exc)[:200]}")
        return
    open_fix = sh("gh", "pr", "list", "--state", "open",
                  "--head", f"fix/pr{pr}-factcheck", "--json", "number").strip()
    fixes = json.loads(open_fix or "[]")
    if fixes:
        # User decision 2026-08-11: fact-check fixes merge automatically; the
        # user reviews the EN version instead. poll_merged sees the fix merge
        # and triggers EN generation (single, existing path).
        num = str(fixes[0]["number"])
        try:
            sh("gh", "pr", "merge", num, "--merge")
            send("核查发现问题，修正已自动并入。英文版随后自动生成——直接等英文版 PR 即可。")
        except Exception as exc:
            send(f"⚠️ 修正 PR 自动合并失败（#{num}），请手动 Merge：{str(exc)[:200]}")
    else:
        sh("git", "fetch", "-q", "origin")
        sh("git", "checkout", "-q", "-B", "master", "origin/master")
        generate_en(slug)


if __name__ == "__main__":
    main()
