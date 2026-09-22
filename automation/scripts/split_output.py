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
    """Extract the payload from model output: prefer the largest fenced block;
    otherwise, if chatter precedes a frontmatter document, cut from the first
    `---` line. Chatter before/after is dropped."""
    text = text.strip()
    blocks = re.findall(r"```[a-zA-Z]*\n(.*?)```", text, re.S)
    if blocks:
        return max(blocks, key=len).strip()
    if not text.startswith("---"):
        m = re.search(r"^---\s*$", text, re.M)
        if m and re.search(r"^(title|slug|lang):", text[m.start():m.start() + 400], re.M):
            return text[m.start():].strip()
    return text


def split_bilingual(text: str, prefix: str) -> None:
    zh = re.search(r"===ZH===\s*(.*?)(?====EN===|$)", text, re.S)
    en = re.search(r"===EN===\s*(.*)$", text, re.S)
    if not zh or not zh.group(1).strip():
        sys.exit("error: no ===ZH=== section found in input")
    Path(f"{prefix}.zh.md").write_text(strip_fences(zh.group(1)))
    if en and en.group(1).strip():
        Path(f"{prefix}.en.md").write_text(strip_fences(en.group(1)))
    print(f"wrote {prefix}.zh.md" + (f" and {prefix}.en.md" if en else " (no EN section)"))


def repair_json(text: str) -> str:
    """Escape ASCII quotes the model left bare inside string values.

    Sonnet wrote 判断"balance of power"接下来 inside a JSON string and the whole
    daily run died at selection with nothing in Discord. A quote inside a
    string is legitimate only when it ends the string — the next non-space
    character is , } ] : or end of text; every other quote gets escaped.
    """
    out, in_str, i, n = [], False, 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "\\" and in_str:
            out.append(text[i:i + 2]); i += 2; continue
        if ch == '"':
            if not in_str:
                in_str = True; out.append(ch); i += 1; continue
            j = i + 1
            while j < n and text[j] in " \t\r\n":
                j += 1
            if j >= n or text[j] in ",}]:":
                in_str = False; out.append(ch)
            else:
                out.append('\\"')
            i += 1; continue
        out.append(ch); i += 1
    return "".join(out)


def parse_json_lenient(text: str):
    import json
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(repair_json(text))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    raw = sys.stdin.read()
    if mode == "json":
        # Emit clean JSON, repairing bare quotes if the model left any; a
        # failure here is loud (non-zero exit) instead of a bad file on disk.
        import json
        try:
            data = parse_json_lenient(strip_fences(raw))
        except Exception as exc:
            sys.stderr.write(f"split_output: model output is not JSON even after repair: {exc}\n")
            sys.stderr.write(strip_fences(raw)[:600] + "\n")
            sys.exit(2)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif mode == "bilingual":
        split_bilingual(raw, sys.argv[2])
    else:
        sys.exit("usage: split_output.py json|bilingual [out_prefix]")
