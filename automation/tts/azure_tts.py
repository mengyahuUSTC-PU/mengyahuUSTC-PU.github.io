#!/usr/bin/env python3
"""Speech synthesis through Azure AI Speech.

Replaces a local Kokoro setup that needed a hand-built Chinese frontend and
still read badly. A commercial engine brings its own frontend, so this file
just sends text — and keeps the books, because the free tier is a monthly
character budget and Azure bills every Chinese character as two.
"""

import html
import json
import os
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

VOICE = os.environ.get("AZURE_TTS_VOICE", "zh-CN-XiaochenMultilingualNeural")
FORMAT = "audio-24khz-48kbitrate-mono-mp3"
MAX_CHARS = 2500      # one request per few paragraphs, well inside the limits
RETRIES = 4
USAGE_DIR = Path("/home/mia/podcast/usage")
FREE_TIER_CHARS = 500_000  # F0: neural characters per month
WARN_AT = 0.8


class QuotaExhausted(RuntimeError):
    """The month's character budget is gone. Retrying is pointless until the
    1st; the caller should park the job and say so."""


def _endpoint() -> str:
    region = os.environ.get("AZURE_SPEECH_REGION", "westus2")
    return f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"


def _chunks(text: str, limit: int = MAX_CHARS):
    """Group paragraphs, never splitting one, so the engine hears whole
    sentences and can phrase them. A single paragraph over the limit is split
    at sentence ends rather than sent whole."""
    out, buf = [], ""
    paragraphs = []
    for para in [p.strip() for p in text.split("\n") if p.strip()]:
        if len(para) <= limit:
            paragraphs.append(para)
            continue
        piece = ""
        for sent in para.replace("。", "。\x00").replace("！", "！\x00").replace("？", "？\x00").split("\x00"):
            if len(piece) + len(sent) > limit and piece:
                paragraphs.append(piece)
                piece = sent
            else:
                piece += sent
        if piece:
            paragraphs.append(piece)
    for para in paragraphs:
        if len(buf) + len(para) > limit and buf:
            out.append(buf)
            buf = para
        else:
            buf = f"{buf}\n{para}" if buf else para
    if buf:
        out.append(buf)
    return out


def _ssml(chunk: str) -> str:
    body = "".join(f"<p>{html.escape(p)}</p>" for p in chunk.split("\n") if p.strip())
    return (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xml:lang="zh-CN"><voice name="{VOICE}">{body}</voice></speak>')


def billable_chars(text: str) -> int:
    """Azure's rule: every code point counts, CJK ideographs count twice."""
    return sum(2 if "一" <= ch <= "鿿" else 1 for ch in text)


def _record_usage(chars: int) -> tuple[int, int]:
    """Running total for the calendar month (UTC, as Azure resets it).
    Returns (month total, budget)."""
    USAGE_DIR.mkdir(parents=True, exist_ok=True)
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    path = USAGE_DIR / f"{month}.json"
    data = json.loads(path.read_text()) if path.exists() else {"chars": 0}
    data["chars"] += chars
    data["updated"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(data))
    return data["chars"], FREE_TIER_CHARS


def month_usage() -> tuple[int, int]:
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    path = USAGE_DIR / f"{month}.json"
    used = json.loads(path.read_text())["chars"] if path.exists() else 0
    return used, FREE_TIER_CHARS


def _speak(chunk: str) -> bytes:
    key = os.environ["AZURE_SPEECH_KEY"]
    headers = {"Ocp-Apim-Subscription-Key": key,
               "Content-Type": "application/ssml+xml",
               "X-Microsoft-OutputFormat": FORMAT,
               "User-Agent": "brand-automation"}
    last = "no attempt made"
    for attempt in range(RETRIES):
        try:
            resp = requests.post(_endpoint(), headers=headers,
                                 data=_ssml(chunk).encode("utf-8"), timeout=180)
        except requests.RequestException as exc:
            # A dropped connection is the commonest transient failure; retry
            # this chunk instead of failing the whole episode and re-billing
            # every chunk on the worker's retry.
            last = f"transport: {exc}"
            time.sleep(2 ** attempt * 5)
            continue
        if resp.status_code == 200:
            return resp.content
        text = resp.text[:300]
        if resp.status_code in (403, 429) and ("quota" in text.lower() or "exceeded" in text.lower()):
            raise QuotaExhausted(f"Azure TTS {resp.status_code}: {text}")
        last = f"Azure TTS {resp.status_code}: {text}"
        if resp.status_code in (429, 500, 502, 503, 504) and attempt < RETRIES - 1:
            time.sleep(2 ** attempt * 5)  # the free tier throttles; back off
            continue
        raise RuntimeError(last)
    raise RuntimeError(f"Azure TTS: retries exhausted ({last})")


def duration_seconds(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def synthesize(text: str, out_mp3: Path) -> float:
    """Speak the whole article into one mp3 (written atomically). Returns its
    length in seconds."""
    chunks = _chunks(text)
    needed = sum(billable_chars(c) for c in chunks)
    used, budget = month_usage()
    if used + needed > budget:
        raise QuotaExhausted(
            f"this episode needs ~{needed:,} billable chars; {used:,}/{budget:,} "
            f"already used this month on the free tier")

    parts = []
    with tempfile.TemporaryDirectory() as tmp:
        for index, chunk in enumerate(chunks):
            part = Path(tmp) / f"{index:03d}.mp3"
            part.write_bytes(_speak(chunk))
            parts.append(part)
        listing = Path(tmp) / "parts.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in parts))
        staged = out_mp3.with_name(out_mp3.name + ".part")
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(listing), "-c", "copy", "-f", "mp3", str(staged)],
            check=True)
        staged.replace(out_mp3)  # never leave a half-written file where nginx can serve it

    total, budget = _record_usage(needed)
    if total >= budget * WARN_AT:
        try:
            import sys
            sys.path.insert(0, "/home/mia/site/automation/scripts")
            from discord_notify import send
            send(f"⚠️ Azure 语音本月已用 {total:,}/{budget:,} 字符（{total/budget:.0%}）。"
                 f"中文按 2 字符计费，超出后当月剩下的朗读版都会失败；升级到 S0 约 $16/百万字符，走 Azure credit。")
        except Exception:
            pass
    return duration_seconds(out_mp3)
