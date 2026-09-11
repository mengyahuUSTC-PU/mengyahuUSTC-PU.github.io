#!/usr/bin/env python3
"""Render queued podcast episodes, one at a time.

PR creation drops a job file in the queue; this worker (cron every five
minutes, also kicked right after a PR opens, always under `flock -n`) drains it
one job at a time. Jobs outlive crashes and reboots; a job that fails is
retried a few times and then parked with its error rather than vanishing.

The render itself is a plain subprocess. It used to be wrapped in
`systemd-run --user` to cap memory when synthesis ran locally; that wrapper
needs a user D-Bus session, which neither cron nor a process kicked from the
Discord poller has, so every render failed with "Failed to connect to bus" and
the string-matched fallback never fired. Synthesis is remote now and light, so
the cap has nothing to protect and is gone.

    podcast_worker.py              drain the queue
    podcast_worker.py --requeue X  move parked job X back into the queue
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

QUEUE = Path("/home/mia/podcast/queue")
FAILED = Path("/home/mia/podcast/failed")
PODCAST = Path(__file__).with_name("podcast.py")
PYTHON = "/home/mia/site/automation/.venv/bin/python"  # same venv as the pipeline
MAX_ATTEMPTS = 3
RETRY_WAIT = 60  # seconds between attempts within one run; a transient API
                 # failure needs time, not three tries in two seconds


def claim_next():
    jobs = sorted(QUEUE.glob("*.json"), key=lambda p: p.stat().st_mtime)
    return jobs[0] if jobs else None


def render(job: dict) -> subprocess.CompletedProcess:
    cmd = [PYTHON, str(PODCAST), job["markdown"]]
    if job.get("pr"):
        cmd += ["--pr", str(job["pr"])]
    if job.get("url"):
        cmd += ["--url", job["url"]]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=1800)


def load_env(path=Path("/home/mia/site/.env")):
    """cron has none of the pipeline's environment, so the render would run
    without the Speech key, the Discord webhook, or the Resend key."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def notify(text: str):
    """Best effort: a failed notice must never change a job's fate."""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from discord_notify import send
        send(text)
    except Exception:
        pass


def park(job: dict, job_file: Path):
    """Keep the job and its markdown together so --requeue has everything."""
    FAILED.mkdir(parents=True, exist_ok=True)
    md = Path(job["markdown"])
    if md.exists() and md.parent == QUEUE:
        md.rename(FAILED / md.name)
        job["markdown"] = str(FAILED / md.name)
    (FAILED / job_file.name).write_text(json.dumps(job, ensure_ascii=False, indent=2))
    job_file.unlink()


def requeue(slug: str) -> bool:
    job_file = FAILED / f"{slug}.json"
    if not job_file.exists():
        print(f"{slug}: nothing parked under that name")
        return False
    job = json.loads(job_file.read_text())
    md = Path(job["markdown"])
    if md.exists() and md.parent == FAILED:
        md.rename(QUEUE / md.name)
        job["markdown"] = str(QUEUE / md.name)
    job["attempts"] = 0
    job.pop("last_error", None)
    QUEUE.mkdir(parents=True, exist_ok=True)
    (QUEUE / job_file.name).write_text(json.dumps(job, ensure_ascii=False, indent=2))
    job_file.unlink()
    print(f"{slug}: back in the queue")
    return True


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--requeue":
        ok = all(requeue(slug) for slug in sys.argv[2:])
        sys.exit(0 if ok else 1)

    load_env()
    QUEUE.mkdir(parents=True, exist_ok=True)
    FAILED.mkdir(parents=True, exist_ok=True)

    while True:
        job_file = claim_next()
        if not job_file:
            return
        job = json.loads(job_file.read_text())
        markdown = Path(job["markdown"])
        if not markdown.exists():
            job["last_error"] = "source markdown is gone"
            park(job, job_file)
            print(f"{job_file.name}: source markdown is gone, parked")
            continue

        started = time.time()
        result = render(job)
        if result.returncode == 0:
            job_file.unlink()
            if markdown.parent == QUEUE:
                markdown.unlink()  # the episode is the artifact now
            print(f"{job['slug']}: done in {time.time()-started:.0f}s")
            print((result.stdout or "").strip()[-400:])
            continue

        job["attempts"] = job.get("attempts", 0) + 1
        job["last_error"] = ((result.stderr or "") + (result.stdout or ""))[-800:]
        if job["attempts"] >= MAX_ATTEMPTS:
            park(job, job_file)
            print(f"{job['slug']}: failed {MAX_ATTEMPTS} times, parked")
            notify(f"⚠️ **朗读版生成失败**（{job['slug']}）试了 {MAX_ATTEMPTS} 次。"
                   f"最后的报错：\n```{job['last_error'][-300:]}```\n"
                   f"修好后在 VM 上跑 `podcast_worker.py --requeue {job['slug']}` 即可重试。")
            continue

        job_file.write_text(json.dumps(job, ensure_ascii=False, indent=2))
        print(f"{job['slug']}: attempt {job['attempts']} failed, retrying in {RETRY_WAIT}s")
        print((result.stderr or "").strip()[-300:])
        time.sleep(RETRY_WAIT)


if __name__ == "__main__":
    main()
