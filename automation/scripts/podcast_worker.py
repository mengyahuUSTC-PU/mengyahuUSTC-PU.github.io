#!/usr/bin/env python3
"""Render queued podcast episodes, one at a time.

Each render peaks around 1.6GB on a 3.9GB box, so two at once is a wedged
machine: on 2026-09-10 three PRs landed within fifteen minutes, three renders
started together, and the VM stopped responding entirely — two of the three
episodes were simply lost, because the old design had no queue at all.

So: PR creation drops a job file here, and this worker (cron, flock -n) drains
the queue one job at a time. Jobs outlive crashes and reboots; a job that fails
is retried a few times and then parked with its error rather than vanishing.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

QUEUE = Path("/home/mia/podcast/queue")
FAILED = Path("/home/mia/podcast/failed")
PODCAST = Path(__file__).with_name("podcast.py")
PYTHON = "/home/mia/tts/.venv/bin/python"
MAX_ATTEMPTS = 3
MEMORY_MAX = "2G"  # a runaway render dies alone instead of taking the box down


def claim_next():
    jobs = sorted(QUEUE.glob("*.json"), key=lambda p: p.stat().st_mtime)
    return jobs[0] if jobs else None


def run(job: dict) -> subprocess.CompletedProcess:
    cmd = ["systemd-run", "--user", "--scope", "-q",
           "-p", f"MemoryMax={MEMORY_MAX}", "-p", "MemorySwapMax=1G",
           PYTHON, str(PODCAST), job["markdown"]]
    if job.get("pr"):
        cmd += ["--pr", str(job["pr"])]
    if job.get("url"):
        cmd += ["--url", job["url"]]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    if result.returncode != 0 and "systemd-run" in (result.stderr or ""):
        # No user session bus under cron: fall back to a plain run. Still
        # serialized, just without the memory ceiling.
        cmd = [PYTHON, str(PODCAST), job["markdown"]]
        if job.get("pr"):
            cmd += ["--pr", str(job["pr"])]
        if job.get("url"):
            cmd += ["--url", job["url"]]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    return result


def main():
    QUEUE.mkdir(parents=True, exist_ok=True)
    FAILED.mkdir(parents=True, exist_ok=True)

    while True:
        job_file = claim_next()
        if not job_file:
            return
        job = json.loads(job_file.read_text())
        markdown = Path(job["markdown"])
        if not markdown.exists():
            job_file.rename(FAILED / job_file.name)
            print(f"{job_file.name}: source markdown is gone")
            continue

        started = time.time()
        result = run(job)
        if result.returncode == 0:
            job_file.unlink()
            print(f"{job['slug']}: done in {(time.time()-started)/60:.1f} min")
            print((result.stdout or "").strip()[-400:])
        else:
            job["attempts"] = job.get("attempts", 0) + 1
            job["last_error"] = (result.stderr or "")[-800:]
            if job["attempts"] >= MAX_ATTEMPTS:
                (FAILED / job_file.name).write_text(json.dumps(job, ensure_ascii=False, indent=2))
                job_file.unlink()
                print(f"{job['slug']}: failed {MAX_ATTEMPTS} times, parked")
                try:
                    sys.path.insert(0, "/home/mia/site/automation/scripts")
                    from discord_notify import send
                    send(f"⚠️ **朗读版生成失败**（{job['slug']}）试了 {MAX_ATTEMPTS} 次。"
                         f"最后的报错：\n```{job['last_error'][-300:]}```")
                except Exception:
                    pass
            else:
                job_file.write_text(json.dumps(job, ensure_ascii=False, indent=2))
                print(f"{job['slug']}: attempt {job['attempts']} failed, will retry")
            return  # leave the rest of the queue for the next tick


if __name__ == "__main__":
    main()
