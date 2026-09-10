#!/usr/bin/env python3
"""Speech synthesis through Azure AI Speech.

Replaces a local Kokoro setup that needed a hand-built Chinese frontend (jieba
segmentation, a polyphone model, a pronunciation table) and still read badly:
wrong phrasing, wrong readings, flat delivery. A commercial engine brings its
own frontend, so all of that is gone — this file just sends text.

It is also ~60x faster than local synthesis, which removes the memory pressure
that wedged the box when several renders overlapped.
"""

import html
import os
import subprocess
import tempfile
import time
from pathlib import Path

import requests

VOICE = os.environ.get("AZURE_TTS_VOICE", "zh-CN-XiaochenMultilingualNeural")
FORMAT = "audio-24khz-48kbitrate-mono-mp3"
MAX_CHARS = 2500      # one request per few paragraphs, well inside the limits
RETRIES = 4


def _endpoint() -> str:
    region = os.environ.get("AZURE_SPEECH_REGION", "westus2")
    return f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"


def _chunks(text: str, limit: int = MAX_CHARS):
    """Group paragraphs, never splitting one, so the engine hears whole
    sentences and can phrase them."""
    out, buf = [], ""
    for para in [p.strip() for p in text.split("\n") if p.strip()]:
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


def _speak(chunk: str) -> bytes:
    key = os.environ["AZURE_SPEECH_KEY"]
    headers = {"Ocp-Apim-Subscription-Key": key,
               "Content-Type": "application/ssml+xml",
               "X-Microsoft-OutputFormat": FORMAT,
               "User-Agent": "brand-automation"}
    for attempt in range(RETRIES):
        resp = requests.post(_endpoint(), headers=headers,
                             data=_ssml(chunk).encode("utf-8"), timeout=180)
        if resp.status_code == 200:
            return resp.content
        # The free tier throttles; back off rather than failing the episode.
        if resp.status_code in (429, 500, 502, 503, 504) and attempt < RETRIES - 1:
            time.sleep(2 ** attempt * 5)
            continue
        raise RuntimeError(f"Azure TTS {resp.status_code}: {resp.text[:200]}")
    raise RuntimeError("Azure TTS: retries exhausted")


def duration_seconds(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def synthesize(text: str, out_mp3: Path) -> float:
    """Speak the whole article into one mp3. Returns its length in seconds."""
    parts = []
    with tempfile.TemporaryDirectory() as tmp:
        for index, chunk in enumerate(_chunks(text)):
            part = Path(tmp) / f"{index:03d}.mp3"
            part.write_bytes(_speak(chunk))
            parts.append(part)

        listing = Path(tmp) / "parts.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in parts))
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(listing), "-c", "copy", str(out_mp3)],
            check=True)
    return duration_seconds(out_mp3)
