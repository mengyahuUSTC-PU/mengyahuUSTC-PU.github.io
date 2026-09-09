#!/usr/bin/env python3
"""Turn a blog post's markdown into text meant to be heard, not read."""

import re


def speech_text(markdown: str) -> str:
    body = markdown
    if body.startswith("---"):
        body = body.split("---", 2)[-1]

    body = re.sub(r"```.*?```", "", body, flags=re.S)          # code blocks
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body)            # images
    body = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", body)        # links: keep the words
    body = re.sub(r"<[^>]+>", "", body)                          # stray html
    body = re.sub(r"^\s{0,3}#{1,6}\s*", "", body, flags=re.M)   # heading marks
    body = re.sub(r"[*_`]{1,3}", "", body)                       # emphasis marks
    body = re.sub(r"^\s*[-*+]\s+", "", body, flags=re.M)        # bullets
    body = re.sub(r"^\s*>\s?", "", body, flags=re.M)            # quotes
    body = re.sub(r"^\s*-{3,}\s*$", "", body, flags=re.M)       # rules
    body = re.sub(r"https?://\S+", "", body)                     # bare urls
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def chunks(text: str, limit: int = 220):
    """Split on sentence ends so each synth call is a natural breath."""
    out, buf = [], ""
    for part in re.split(r"(?<=[。！？；.!?])\s*", text):
        part = part.strip()
        if not part:
            continue
        if len(buf) + len(part) > limit and buf:
            out.append(buf)
            buf = part
        else:
            buf = f"{buf} {part}".strip()
    if buf:
        out.append(buf)
    return out


LATIN_RUN = re.compile(r"[A-Za-z][A-Za-z0-9''\-\.]*(?:\s+[A-Za-z][A-Za-z0-9''\-\.]*)*")


def split_runs(text: str):
    """Yield ('zh'|'en', piece). Only runs long enough to be worth switching
    voices for are treated as English; a stray 'AI' stays in the Chinese run."""
    out, last = [], 0
    for m in LATIN_RUN.finditer(text):
        run = m.group(0)
        if len(run) < 12 or " " not in run:      # short token: let the zh voice say it
            continue
        if m.start() > last:
            out.append(("zh", text[last:m.start()]))
        out.append(("en", run))
        last = m.end()
    if last < len(text):
        out.append(("zh", text[last:]))
    return [(lang, piece.strip()) for lang, piece in out if piece.strip()]
