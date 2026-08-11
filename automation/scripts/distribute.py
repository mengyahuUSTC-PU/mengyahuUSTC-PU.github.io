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


def gen_sections(prompt: str, names: list[str], alias: dict | None = None) -> dict:
    """Generate and parse ===NAME=== sections; on missing sections, retry once
    with the failure fed back so the model can fix its own formatting.
    A user-feedback note aimed at one part must never sink the whole run."""
    alias = alias or {}
    for attempt in (1, 2):
        raw = claude_gen(prompt)
        out = {}
        for n in names:
            out[n] = section(raw, n) or (section(raw, alias[n]) if n in alias else "")
        missing = [n for n in names if not out[n]]
        if not missing:
            return out
        if attempt == 1:
            markers = " ".join(f"==={n}===" for n in names)
            prompt = (prompt
                      + "\n\n## 格式错误警告（第二次尝试）\n"
                      + f"上一次输出缺少段标记：{', '.join(missing)}。"
                      + f"最终回复必须且只包含全部段落（{markers}），"
                      + "即使某段内容无需修改也必须完整输出该段，不要输出任何解说。")
    sys.exit(f"error: generation missing sections after retry: {', '.join(missing)}")


def section(text: str, name: str) -> str:
    m = re.search(rf"==={name}===\s*(.*?)(?====[A-Z_]+===|$)", text, re.S)
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
    social = gen_sections(
        baseline + "\n\n" + (PROMPTS / "social-en.md").read_text() + fb
        + f"\n\n## X 帖 UTM 链接\n{utm(slug, 'en', 'twitter', 'post')}"
        + f"\n\n## LinkedIn 版 UTM 链接\n{utm(slug, 'en', 'linkedin', 'post')}"
        + "\n\n## 文章全文\n\n" + en.read_text(),
        ["X", "LINKEDIN"], alias={"X": "THREAD"},
    )
    thread, linkedin = social["X"], social["LINKEDIN"]

    # --- Newsletter emails (zh + en), only when both language versions exist ---
    email = None
    zh = REPO_ROOT / "src" / "content" / "blog" / "zh" / f"{slug}.md"
    if zh.exists():
        news = gen_sections(
            baseline + "\n\n" + (PROMPTS / "newsletter.md").read_text() + fb
            + f"\n\n## 中文版 UTM 链接\n{utm(slug, 'zh', 'newsletter', 'email')}"
            + f"\n\n## 英文版 UTM 链接\n{utm(slug, 'en', 'newsletter', 'email')}"
            + "\n\n## 中文版全文\n\n" + zh.read_text()
            + "\n\n## 英文版全文\n\n" + en.read_text(),
            ["SUBJECT_ZH", "HTML_ZH", "SUBJECT_EN", "HTML_EN"],
        )
        email = {
            "zh": {"subject": news["SUBJECT_ZH"], "html": news["HTML_ZH"]},
            "en": {"subject": news["SUBJECT_EN"], "html": news["HTML_EN"]},
        }

    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / f"{slug}.json").write_text(
        json.dumps({"slug": slug, "thread": thread, "linkedin": linkedin,
                    "email": email, "status": "pending"},
                   ensure_ascii=False, indent=2)
    )

    # --- Discord preview ---
    send(f"🐦 **X 帖预览（单条）**（{slug}）\n\n{thread}")
    send(f"💼 **LinkedIn 帖预览**（{slug}）\n\n{linkedin}")
    if email:
        send(
            f"📧 **Newsletter 预览**（{slug}）\n\n"
            f"**中文主题**：{email['zh']['subject']}\n```{email['zh']['html']}```\n"
            f"**EN subject**: {email['en']['subject']}\n```{email['en']['html']}```"
        )
    steps = "thread + LinkedIn 排进 Typefully" + (
        " + newsletter 发给订阅者" if email else "")
    send(
        f"⏸ 以上是 **{slug}** 的分发队列（未排程）。\n"
        f"回复 `定时发 {slug}`（推荐：高峰时段数据更好）或 `发 {slug}` 立即发 → {steps}。不回复则不排程。"
    )
    print(f"distribution pack ready for {slug}")


if __name__ == "__main__":
    main()
