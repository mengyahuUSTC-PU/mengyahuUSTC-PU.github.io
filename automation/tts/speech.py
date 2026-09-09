#!/usr/bin/env python3
"""Chinese-first text to Kokoro phonemes, with English pronounced as English.

Two decisions here, both from listening to the output:

1. One voice reads everything. Switching to an English voice for a stray "AI"
   sounds worse than a single reader, so the mixing happens at the phoneme
   level instead: Chinese and English phonemes are spliced into one string and
   spoken by the same Chinese voice.

2. Polyphones are resolved by a model, not by rules. misaki reads pinyin per
   jieba token, so any word jieba does not know decays to the character's
   default reading: 重发 became zhòng fā, 说得 became dé, 变形为 became wèi.
   g2pW picks the reading from context and gets those right.
"""

import json
import re
from functools import lru_cache
from pathlib import Path

from kokoro_onnx.tokenizer import Tokenizer
from misaki.transcription import pinyin_to_ipa

_tokenizer = Tokenizer()
_converter = None

OVERRIDES_FILE = Path(__file__).with_name("pronunciation.json")

# Letter names as IPA. Spelling them out for the English phonemizer is not
# reliable ("ay" comes back as /aɪ/, which turns AI into "eye eye").
LETTER_IPA = {
    "A": "ˈeɪ", "B": "bˈiː", "C": "sˈiː", "D": "dˈiː", "E": "ˈiː", "F": "ˈɛf",
    "G": "dʒˈiː", "H": "ˈeɪtʃ", "I": "ˈaɪ", "J": "dʒˈeɪ", "K": "kˈeɪ",
    "L": "ˈɛl", "M": "ˈɛm", "N": "ˈɛn", "O": "ˈoʊ", "P": "pˈiː", "Q": "kjˈuː",
    "R": "ˈɑːɹ", "S": "ˈɛs", "T": "tˈiː", "U": "jˈuː", "V": "vˈiː",
    "W": "dˈʌbəljuː", "X": "ˈɛks", "Y": "wˈaɪ", "Z": "zˈiː",
}

SAID_AS_WORD = {"NASA", "OPEC", "AWS", "SQL", "JSON", "GIF"}

LATIN = re.compile(r"[A-Za-z][A-Za-z0-9'’\-\.]*")
HAN = re.compile(r"[一-鿿]")

TONE_MARKS = (("˧˩˧", "↓"), ("˧˥", "↗"), ("˥˩", "↘"), ("˥", "→"))


@lru_cache(maxsize=1)
def _load_overrides() -> tuple:
    """Chinese phrases this pipeline says often that a general model still gets
    wrong. Kept as a file so a misreading heard in an episode can be corrected
    without touching code. Longest first, so 调用接口 wins over 调用."""
    if not OVERRIDES_FILE.exists():
        return ()
    data = json.loads(OVERRIDES_FILE.read_text())
    return tuple(sorted(data.items(), key=lambda kv: -len(kv[0])))


def _g2p():
    global _converter
    if _converter is None:
        from g2pw import G2PWConverter
        _converter = G2PWConverter(style="pinyin", enable_non_tradional_chinese=True)
    return _converter


def _is_acronym(token: str) -> bool:
    letters = re.sub(r"[^A-Za-z]", "", token)
    if not letters or token.upper() in SAID_AS_WORD:
        return False
    return letters.isupper() and len(letters) <= 5


@lru_cache(maxsize=4096)
def _en_phonemes(token: str) -> str:
    if not _is_acronym(token):
        return _tokenizer.phonemize(token.replace("-", " "), lang="en-us").strip()
    out = []
    for ch in token:
        if ch.isalpha():
            out.append(LETTER_IPA[ch.upper()])
        elif ch.isdigit():
            out.append(_tokenizer.phonemize(ch, lang="en-us").strip())
    return " ".join(out)


def _ipa(pinyin: str) -> str:
    """One pinyin syllable (e.g. 'zhong4') to Kokoro's phoneme spelling."""
    try:
        ipa = "".join(next(iter(pinyin_to_ipa(pinyin))))
    except Exception:
        return ""
    for tone, arrow in TONE_MARKS:
        ipa = ipa.replace(tone, arrow)
    return ipa


@lru_cache(maxsize=1)
def _fallback_g2p():
    from misaki import zh
    return zh.ZHG2P()


def _chinese_phonemes(text: str) -> str:
    overrides = dict(_load_overrides())
    for word, _ in _load_overrides():
        # Marked before the model runs, so a domain word wins over the general
        # case without the model ever seeing it.
        text = text.replace(word, f"\x00{word}\x00")

    parts = []
    for segment in text.split("\x00"):
        if not segment:
            continue
        if segment in overrides:
            parts.append(" ".join(_ipa(p) for p in overrides[segment]))
            continue
        readings = _g2p()([segment])[0]
        chars = [c for c in segment if HAN.match(c)]
        syllables = [r for r in readings if r]
        if len(syllables) == len(chars):
            parts.append(" ".join(_ipa(s) for s in syllables))
        else:
            # g2pW only returns readings for Han characters; fall back for the
            # rest of the segment so punctuation and digits are not dropped.
            parts.append(_fallback_g2p()(segment)[0])
    return " ".join(p for p in parts if p)


def mixed_phonemes(text: str) -> str:
    """Phonemes for a Chinese sentence that has English words in it."""
    parts, last = [], 0
    for match in LATIN.finditer(text):
        token = match.group(0).strip(".")
        if not token:
            continue
        if match.start() > last:
            chinese = text[last:match.start()]
            if HAN.search(chinese):
                parts.append(_chinese_phonemes(chinese))
        parts.append(_en_phonemes(token))
        last = match.end()
    if last < len(text):
        tail = text[last:]
        if HAN.search(tail):
            parts.append(_chinese_phonemes(tail))
    return " ".join(p for p in parts if p)
