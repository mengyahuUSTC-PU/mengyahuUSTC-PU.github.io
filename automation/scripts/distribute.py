#!/usr/bin/env python3
"""Generate distribution content for a published article and preview it on Discord.

Usage: distribute.py <slug>

Reads src/content/blog/en/<slug>.md and zh/<slug>.md, generates:
  - EN Twitter thread + LinkedIn post  -> automation/data/dist/<slug>.json

Everything is previewed in Discord. Nothing is scheduled until the user
replies "发 <slug>" (handled by poll_discord.py).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "automation" / "scripts"
PROMPTS = REPO_ROOT / "automation" / "prompts"
DIST = REPO_ROOT / "automation" / "data" / "dist"
SITE = "https://mengyahuustc-pu.github.io"

sys.path.insert(0, str(SCRIPTS))
from discord_notify import load_env, send  # noqa: E402


def utm(slug: str, lang: str, source: str, medium: str) -> str:
    return (
        f"{SITE}/{lang}/{slug}/?utm_source={source}"
        f"&utm_medium={medium}&utm_campaign={slug}"
    )


def claude_gen(prompt: str) -> str:
    run = subprocess.run(
        ["claude", "-p", "--output-format", "text",
         "--model", "fable", "--fallback-model", "opus"],
        input=prompt, cwd=REPO_ROOT, capture_output=True, text=True, timeout=900,
    )
    if run.returncode != 0:
        raise RuntimeError(f"claude failed: {(run.stderr or run.stdout)[-300:]}")
    return run.stdout


def section(text: str, name: str) -> str:
    m = re.search(rf"==={name}===\s*(.*?)(?====[A-Z]+===|$)", text, re.S)
    return m.group(1).strip() if m else ""


def main():
    slug = sys.argv[1]
    feedback = sys.argv[2] if len(sys.argv) > 2 else ""
    load_env()
    en = REPO_ROOT / "src" / "content" / "blog" / "en" / f"{slug}.md"
    if not en.exists():
        sys.exit(f"error: {en} not found")

    baseline = (
        (PROMPTS / "editorial-baseline.md").read_text()
        + "\n\n" + (PROMPTS / "editorial-lessons.md").read_text()
    )

    # --- EN social (thread + LinkedIn) ---
    fb = f"\n\n## 用户对上一版的修改意见（必须遵守）\n\n{feedback}" if feedback else ""
    social_raw = claude_gen(
        baseline + "\n\n" + (PROMPTS / "social-en.md").read_text() + fb
        + f"\n\n## Thread 版 UTM 链接\n{utm(slug, 'en', 'twitter', 'thread')}"
        + f"\n\n## LinkedIn 版 UTM 链接\n{utm(slug, 'en', 'linkedin', 'post')}"
        + "\n\n## 文章全文\n\n" + en.read_text()
    )
    thread = section(social_raw, "THREAD")
    linkedin = section(social_raw, "LINKEDIN")
    if not thread or not linkedin:
        sys.exit("error: social generation missing THREAD/LINKEDIN sections")

    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / f"{slug}.json").write_text(
        json.dumps({"slug": slug, "thread": thread, "linkedin": linkedin,
                    "status": "pending"}, ensure_ascii=False, indent=2)
    )

    # --- Discord preview ---
    tweets = [t.strip() for t in thread.split("\n\n") if t.strip()]
    thread_preview = "\n\n".join(f"**{i}.** {t}" for i, t in enumerate(tweets, 1))
    send(f"🐦 **Twitter thread 预览**（{slug}）\n\n{thread_preview}")
    send(f"💼 **LinkedIn 帖预览**（{slug}）\n\n{linkedin}")
    send(
        f"⏸ 以上是 **{slug}** 的分发队列（未排程）。\n"
        f"回复 `发 {slug}` → thread + LinkedIn 排进 Typefully。不回复则不排程。"
    )
    print(f"distribution pack ready for {slug}")


if __name__ == "__main__":
    main()
