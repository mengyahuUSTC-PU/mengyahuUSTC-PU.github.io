#!/usr/bin/env python3
"""Render queued podcast episodes, one at a time.

PR creation drops a job file in the queue; this worker (cron every five
minutes, also kicked right after a PR opens) drains it one job at a time.
Jobs outlive crashes and reboots; a job that fails is retried a few times and
then parked with its error rather than vanishing. Nothing a single bad job can
do — malformed file, missing source, render hang, quota gone — is allowed to
stall the jobs behind it or crash the loop.

    podcast_worker.py              drain the queue
    podcast_worker.py --requeue X  move parked job X back into the queue
"""

import fcntl
import json
import os
import subprocess
import sys
import time
from pathlib import Path

QUEUE = Path("/home/mia/podcast/queue")
WORKING = Path("/home/mia/podcast/working")
FAILED = Path("/home/mia/podcast/failed")
LOCK = Path("/tmp/podcast-worker.lock")
PODCAST = Path(__file__).with_name("podcast.py")
PYTHON = "/home/mia/site/automation/.venv/bin/python"  # same venv as the pipeline
MAX_ATTEMPTS = 3
RETRY_WAIT = 60      # a transient API failure needs time, not three tries in two seconds
RENDER_TIMEOUT = 1800
QUOTA_MARK = "QuotaExhausted"


def claim_next():
    """Move the oldest job into working/ so a re-enqueue of the same slug
    while it renders lands in queue/ untouched instead of being deleted with
    the finished job."""
    for job_file in sorted(QUEUE.glob("*.json"), key=lambda p: p.stat().st_mtime):
        try:
            job = json.loads(job_file.read_text())
            slug = job["slug"]
            src = Path(job["markdown"])
        except Exception as exc:  # noqa: BLE001 — a bad file must not stall the queue
            FAILED.mkdir(parents=True, exist_ok=True)
            job_file.rename(FAILED / job_file.name)
            print(f"{job_file.name}: unreadable job file, parked ({exc})")
            continue
        WORKING.mkdir(parents=True, exist_ok=True)
        if src.exists() and src.parent == QUEUE:
            src.rename(WORKING / src.name)
            job["markdown"] = str(WORKING / src.name)
        working = WORKING / job_file.name
        working.write_text(json.dumps(job, ensure_ascii=False, indent=2))
        job_file.unlink()
        return working, job
    return None, None


def render(job: dict) -> subprocess.CompletedProcess:
    cmd = [PYTHON, str(PODCAST), job["markdown"]]
    if job.get("pr"):
        cmd += ["--pr", str(job["pr"])]
    if job.get("url"):
        cmd += ["--url", job["url"]]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=RENDER_TIMEOUT)
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(cmd, 124, exc.stdout or "",
                                           f"render exceeded {RENDER_TIMEOUT}s and was killed")


def load_env(path=Path("/home/mia/site/.env")):
    """cron has none of the pipeline's environment."""
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
    job["parked_month"] = month_stamp()
    md = Path(job["markdown"])
    if md.exists() and md.parent in (QUEUE, WORKING):
        md.rename(FAILED / md.name)
        job["markdown"] = str(FAILED / md.name)
    (FAILED / job_file.name).write_text(json.dumps(job, ensure_ascii=False, indent=2))
    job_file.unlink(missing_ok=True)


def back_to_queue(job: dict, job_file: Path):
    """Return a job to the queue for a later attempt (same file name, so a
    re-enqueue that happened meanwhile wins by being newer)."""
    md = Path(job["markdown"])
    if md.exists() and md.parent == WORKING:
        md.rename(QUEUE / md.name)
        job["markdown"] = str(QUEUE / md.name)
    target = QUEUE / job_file.name
    if not target.exists():  # a fresh enqueue for this slug replaces the retry
        target.write_text(json.dumps(job, ensure_ascii=False, indent=2))
    job_file.unlink(missing_ok=True)


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


def month_stamp() -> str:
    return time.strftime("%Y-%m", time.gmtime())  # Azure resets the quota on UTC month boundaries


def revive_after_quota_reset():
    """Jobs parked because the month's free characters ran out come back on
    their own once the month changes — the owner chose the free tier and does
    not want to babysit it."""
    for job_file in FAILED.glob("*.json"):
        try:
            job = json.loads(job_file.read_text())
        except Exception:
            continue
        if QUOTA_MARK not in (job.get("last_error") or "") and job.get("last_error") != "parked with the quota exhaustion":
            continue
        if job.get("parked_month") == month_stamp():
            continue  # still the month that ran dry
        requeue(job["slug"])
        print(f"{job['slug']}: quota reset, back in the queue")


def recover_working():
    """Anything left in working/ belonged to a worker that died mid-render
    (reboot, kill). Put it back so it is retried, not forgotten."""
    for job_file in WORKING.glob("*.json"):
        try:
            job = json.loads(job_file.read_text())
        except Exception:
            job_file.rename(FAILED / job_file.name)
            continue
        back_to_queue(job, job_file)
        print(f"{job_file.stem}: recovered from an interrupted run")


def drain():
    QUEUE.mkdir(parents=True, exist_ok=True)
    WORKING.mkdir(parents=True, exist_ok=True)
    FAILED.mkdir(parents=True, exist_ok=True)
    revive_after_quota_reset()
    recover_working()

    while True:
        job_file, job = claim_next()
        if not job_file:
            return
        markdown = Path(job["markdown"])
        if not markdown.exists():
            job["last_error"] = "source markdown is gone"
            park(job, job_file)
            print(f"{job['slug']}: source markdown is gone, parked")
            continue

        started = time.time()
        result = render(job)
        if result.returncode == 0:
            job_file.unlink()
            markdown.unlink(missing_ok=True)  # the episode is the artifact now
            print(f"{job['slug']}: done in {time.time()-started:.0f}s")
            print((result.stdout or "").strip()[-400:])
            continue

        err = ((result.stderr or "") + (result.stdout or ""))[-800:]
        job["attempts"] = job.get("attempts", 0) + 1
        job["last_error"] = err

        if QUOTA_MARK in err:
            # Deterministic until the month rolls over: park every job now
            # rather than burning three attempts each and hammering the API.
            park(job, job_file)
            print(f"{job['slug']}: Azure quota exhausted, parked")
            notify(f"🚨 **朗读版暂停：Azure 语音本月免费额度用完了**（{job['slug']} 已停放）。\n"
                   f"不会产生任何费用：停放的任务会在下月 1 号自动重新渲染。\n"
                   f"如果想现在就恢复，那是额外消费（升到 S0，按目前用量每月约 $9，走 Azure credit）——"
                   f"回复「升级语音」我再动，不回复就等下月。")
            for other_file in list(QUEUE.glob("*.json")):
                try:
                    other = json.loads(other_file.read_text())
                    other["last_error"] = "parked with the quota exhaustion"
                    park(other, other_file)
                except Exception:
                    pass
            return

        if job["attempts"] >= MAX_ATTEMPTS:
            park(job, job_file)
            print(f"{job['slug']}: failed {MAX_ATTEMPTS} times, parked")
            notify(f"⚠️ **朗读版生成失败**（{job['slug']}）试了 {MAX_ATTEMPTS} 次。"
                   f"最后的报错：\n```{err[-300:]}```\n"
                   f"修好后在 VM 上跑 `podcast_worker.py --requeue {job['slug']}` 即可重试。")
            continue

        print(f"{job['slug']}: attempt {job['attempts']} failed, retrying in {RETRY_WAIT}s")
        print((result.stderr or "").strip()[-300:])
        time.sleep(RETRY_WAIT)
        back_to_queue(job, job_file)


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--requeue":
        ok = all(requeue(slug) for slug in sys.argv[2:])
        sys.exit(0 if ok else 1)

    load_env()
    # The callers use flock -n too, but a worker started by hand must not race
    # the cron one either: take the same lock here.
    with LOCK.open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("another worker holds the lock; leaving the queue to it")
            return
        try:
            drain()
        except Exception as exc:  # noqa: BLE001 — the loop's last line of defence
            print(f"worker crashed: {exc!r}")
            notify(f"🚨 朗读 worker 异常退出：`{exc!r}`，队列里的任务会在下个 5 分钟被重新拾起。")
            raise


if __name__ == "__main__":
    main()
