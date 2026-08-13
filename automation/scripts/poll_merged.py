#!/usr/bin/env python3
"""Post-merge orchestrator. Runs from cron and reacts to merged PRs:

- post/<slug> (zh deep dive) merged  -> three-model fact-check (user iterates
  BEFORE merging; audit happens after). Issues -> fix PR to Discord; clean ->
  generate the English version immediately.
- fix/* merged whose files include a zh article without an EN counterpart
  -> generate the English version (audit round finished).
- post/<slug>-en merged -> distribution content generation.
- post/briefing-* merged -> nothing (briefings are audited pre-review).

State (processed PR numbers) lives in automation/data/state/merged.json.
"""

import json
import re
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


def zh_path(slug):
    return REPO_ROOT / "src" / "content" / "blog" / "zh" / f"{slug}.md"


def en_path(slug):
    return REPO_ROOT / "src" / "content" / "blog" / "en" / f"{slug}.md"


def generate_en(slug: str) -> bool:
    """EN native rewrite from the (audited) zh version; opens the EN PR."""
    send(f"🌐 中文版已定稿（{slug}），开始生成英文版…")
    prompt = (
        (PROMPTS / "editorial-baseline.md").read_text()
        + "\n\n" + (PROMPTS / "editorial-lessons.md").read_text()
        + "\n\n" + (PROMPTS / "en-version.md").read_text()
        + "\n\n## 已发布的中文版全文\n\n" + zh_path(slug).read_text()
    )
    raw = None
    for attempt in (1, 2):
        run = subprocess.run(
            ["claude", "-p", "--output-format", "text",
             "--model", "fable", "--fallback-model", "opus",
             "--allowedTools", "WebFetch", "WebSearch"],
            input=prompt, cwd=REPO_ROOT, capture_output=True, text=True, timeout=900,
        )
        if run.returncode == 0:
            raw = run.stdout
            break
        if attempt == 1:
            time.sleep(60)
    if raw is None:
        send(f"⚠️ 英文版生成失败（{slug}）：\n```{(run.stderr or run.stdout)[-400:]}```")
        return False
    clean = subprocess.run(
        [sys.executable, str(SCRIPTS / "split_output.py"), "json"],
        input=raw, check=True, capture_output=True, text=True,
    ).stdout
    draft = REPO_ROOT / "automation" / "drafts" / f"{slug}.en.md"
    draft.write_text(clean)
    try:
        pr_url = subprocess.run(
            [sys.executable, str(SCRIPTS / "make_pr.py"), str(draft)],
            cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=300,
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        send(f"⚠️ 英文版 PR 创建失败（{slug}）：\n```{(exc.stderr or str(exc))[-400:]}```")
        return False
    m = re.search(r"/pull/(\d+)", pr_url)
    en_pr = m.group(1) if m else None
    audit_clone = Path("/home/mia/site-audit")
    if en_pr and audit_clone.exists():
        # User decision 2026-08-11: EN is verified and merged automatically.
        send(f"📬 英文版 PR 已开：{pr_url}\n核查中，通过后自动上线（无需操作），随后发分发预览。")
        py = "/home/mia/site/automation/.venv/bin/python"
        cmd = (f"nohup flock /tmp/audit-git.lock bash -c "
               f"'cd {audit_clone} && git fetch -q origin && "
               f"git checkout -q -B master origin/master && "
               f"{py} automation/scripts/audit_and_continue.py {en_pr} {slug} en' "
               f">> /home/mia/audit.log 2>&1 &")
        subprocess.Popen(cmd, shell=True)
    else:
        send(f"📬 英文版 PR 已开：{pr_url}\n（基于审计后的中文终稿原生重写）Merge 后自动生成分发内容。")
    return True


def run_audit(pr_number: int) -> str:
    """Run the three-model fact-check on a merged PR.
    Returns "fix_pr" | "clean" | "error"."""
    run = subprocess.run(
        [sys.executable, str(SCRIPTS / "verify_draft.py"), str(pr_number)],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=2400,
    )
    if run.returncode != 0:
        send(f"⚠️ 三方核查运行失败（PR #{pr_number}）：\n```{(run.stderr or run.stdout)[-400:]}```")
        return "error"
    open_fix = sh("gh", "pr", "list", "--state", "open",
                  "--head", f"fix/pr{pr_number}-factcheck", "--json", "number").strip()
    return "fix_pr" if json.loads(open_fix or "[]") else "clean"


def main():
    load_env()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"done": []}

    prs = json.loads(
        sh("gh", "pr", "list", "--state", "merged", "--limit", "20",
           "--json", "number,headRefName,title,files")
    )
    sh("git", "checkout", "-q", "master")
    sh("git", "pull", "-q", "origin", "master")

    for pr in prs:
        branch, number = pr["headRefName"], pr["number"]
        if number in state["done"]:
            continue

        # EN post merged -> distribution pack.
        if branch.startswith("post/") and branch.endswith("-en"):
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

        # Briefings are audited before review; just confirm publication.
        if branch.startswith("post/briefing-"):
            date_part = branch.removeprefix("post/briefing-")
            send(f"✅ {date_part} 快讯已合并，网站部署中（约 2 分钟后上线）："
                 f"https://mengyahu.com/zh/briefing-{date_part}/")
            state["done"].append(number)
            continue

        # zh deep dive merged -> post-merge audit. Runs in the dedicated
        # audit clone (own lock) so it never blocks revisions/polls here.
        if branch.startswith("post/"):
            slug = branch.removeprefix("post/")
            if not zh_path(slug).exists() or en_path(slug).exists():
                state["done"].append(number)
                continue
            audit_clone = Path("/home/mia/site-audit")
            if audit_clone.exists():
                send(f"🔍 {slug} 已合并，三方核查已在并行通道启动（不阻塞其他任务）…")
                py = "/home/mia/site/automation/.venv/bin/python"
                cmd = (f"nohup flock /tmp/audit-git.lock bash -c "
                       f"'cd {audit_clone} && git fetch -q origin && "
                       f"git checkout -q -B master origin/master && "
                       f"{py} automation/scripts/audit_and_continue.py {number} {slug}' "
                       f">> /home/mia/audit.log 2>&1 &")
                subprocess.Popen(cmd, shell=True)
                state["done"].append(number)
            else:
                send(f"🔍 {slug} 已合并，启动三方核查（Opus + Fable + GPT）…")
                outcome = run_audit(number)
                if outcome == "fix_pr":
                    send("核查发现问题，修正 PR 已开（见上方链接）。**Merge 修正后我再生成英文版。**")
                    state["done"].append(number)
                elif outcome == "clean":
                    generate_en(slug)
                    state["done"].append(number)
                # on "error": leave un-done so the next cron retries
            continue

        # Audit fix PR merged -> the zh text is final; generate EN if missing.
        if branch.startswith("fix/"):
            for f in pr.get("files", []):
                m = re.match(r"src/content/blog/zh/(.+)\.md$", f["path"])
                if m and not en_path(m.group(1)).exists():
                    generate_en(m.group(1))
            state["done"].append(number)
            continue

        state["done"].append(number)

    STATE_FILE.write_text(json.dumps(state))


if __name__ == "__main__":
    main()
