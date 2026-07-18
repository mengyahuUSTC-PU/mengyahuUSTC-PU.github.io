#!/usr/bin/env python3
"""Helpers to post-process claude -p output.

Usage:
  split_output.py json  < raw > clean.json     # strip ``` fences around JSON
  split_output.py bilingual OUT_PREFIX < raw   # split ===ZH===/===EN=== into
                                               # OUT_PREFIX.zh.md / OUT_PREFIX.en.md
"""

import re
import sys
from pathlib import Path


def strip_fences(text: str) -> str:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    return m.group(1).strip() if m else text


def split_bilingual(text: str, prefix: str) -> None:
    zh = re.search(r"===ZH===\s*(.*?)(?====EN===|$)", text, re.S)
    en = re.search(r"===EN===\s*(.*)$", text, re.S)
    if not zh or not zh.group(1).strip():
        sys.exit("error: no ===ZH=== section found in input")
    Path(f"{prefix}.zh.md").write_text(strip_fences(zh.group(1)))
    if en and en.group(1).strip():
        Path(f"{prefix}.en.md").write_text(strip_fences(en.group(1)))
    print(f"wrote {prefix}.zh.md" + (f" and {prefix}.en.md" if en else " (no EN section)"))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    raw = sys.stdin.read()
    if mode == "json":
        print(strip_fences(raw))
    elif mode == "bilingual":
        split_bilingual(raw, sys.argv[2])
    else:
        sys.exit("usage: split_output.py json|bilingual [out_prefix]")
