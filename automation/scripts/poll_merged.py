#!/usr/bin/env python3
"""Detect merged Chinese post PRs and auto-generate the English-version PR.

Runs from cron. For every merged PR on a post/* branch where the repo now has
src/content/blog/zh/<slug>.md but no en/<slug>.md, generates the English
version with claude -p and opens a second PR on branch post/<slug>-en.

State (processed PR numbers) lives in automation/data/state/merged.json.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "automation" / "data"
STATE_FILE = DATA / "state" / "merged.json"
SCRIPTS = REPO_ROOT / "automation" / "scripts"
PROMPTS = REPO_ROOT / "automation" / "prompts"

sys.path.insert(0, str(SCRIPTS))
from discord_notify import load_env, send  # noqa: E402


def sh(*cmd, timeout=600):
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=timeout
    ).stdout


def main():
    load_env()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"done": []}

    prs = json.loads(
        sh("gh", "pr", "list", "--state", "merged", "--limit", "20",
           "--json", "number,headRefName,title")
    )
    sh("git", "checkout", "-q", "master")
    sh("git", "pull", "-q", "origin", "master")

    for pr in prs:
        branch, number = pr["headRefName"], pr["number"]
        if number in state["done"] or not branch.startswith("post/"):
            continue
        # Merged EN post -> kick off distribution (thread/LinkedIn/XHS preview).
        if branch.endswith("-en"):
            slug = branch.removeprefix("post/").removesuffix("-en")
            try:
                subprocess.run(
                    [sys.executable, str(SCRIPTS / "distribute.py"), slug],
                    cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=1200,
                )
                state["done"].append(number)
            except subprocess.CalledProcessError as exc:
                send(f"⚠️ 分发内容生成失败（{slug}）：\n```{(exc.stderr or str(exc))[-500:]}```")
            continue
        slug = branch.removeprefix("post/")
        zh = REPO_ROOT / "src" / "content" / "blog" / "zh" / f"{slug}.md"
        en = REPO_ROOT / "src" / "content" / "blog" / "en" / f"{slug}.md"
        if not zh.exists() or en.exists():
            state["done"].append(number)
            continue

        send(f"🌐 检测到中文版已合并（{slug}），开始生成英文版…")
        prompt = (
            (PROMPTS / "editorial-baseline.md").read_text()
            + "\n\n" + (PROMPTS / "editorial-lessons.md").read_text()
            + "\n\n" + (PROMPTS / "en-version.md").read_text()
            + "\n\n## 已发布的中文版全文\n\n" + zh.read_text()
        )
        try:
            raw = None
            for attempt in (1, 2):
                run = subprocess.run(
                    ["claude", "-p", "--output-format", "text",
                     "--allowedTools", "WebFetch", "WebSearch"],
                    input=prompt, cwd=REPO_ROOT,
                    capture_output=True, text=True, timeout=900,
                )
                if run.returncode == 0:
                    raw = run.stdout
                    break
                if attempt == 1:
                    time.sleep(60)
            if raw is None:
                raise subprocess.CalledProcessError(
                    run.returncode, run.args,
                    output=run.stdout, stderr=run.stderr or run.stdout,
                )
            clean = subprocess.run(
                [sys.executable, str(SCRIPTS / "split_output.py"), "json"],
                input=raw, check=True, capture_output=True, text=True,
            ).stdout
            draft = REPO_ROOT / "automation" / "drafts" / f"{slug}.en.md"
            draft.write_text(clean)
            pr_url = subprocess.run(
                [sys.executable, str(SCRIPTS / "make_pr.py"), str(draft)],
                cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=300,
            ).stdout.strip()
            send(f"📬 英文版 PR 已开：{pr_url}")
            state["done"].append(number)
        except subprocess.CalledProcessError as exc:
            send(f"⚠️ 英文版生成失败（{slug}）：\n```{(exc.stderr or str(exc))[-500:]}```")

    STATE_FILE.write_text(json.dumps(state))


if __name__ == "__main__":
    main()
