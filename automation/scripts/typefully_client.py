#!/usr/bin/env python3
"""Minimal Typefully API client.

Docs: https://support.typefully.com/en/articles/8718287-typefully-api
Auth: X-API-KEY header, key from TYPEFULLY_API_KEY (env or .env).
"""

import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from discord_notify import load_env  # noqa: E402

BASE = "https://api.typefully.com/v1"


def _key():
    load_env()
    key = os.environ.get("TYPEFULLY_API_KEY")
    if not key:
        sys.exit("error: TYPEFULLY_API_KEY not set (env or .env)")
    return key


def create_draft(content: str, schedule_date: str | None = None, threadify: bool = False):
    """Create a draft. content: tweets separated by 4 newlines for threads.
    schedule_date: ISO-8601 UTC string, or None to leave as unscheduled draft."""
    payload = {"content": content, "threadify": threadify, "share": True}
    if schedule_date:
        payload["schedule-date"] = schedule_date
    resp = requests.post(
        f"{BASE}/drafts/",
        headers={"X-API-KEY": f"Bearer {_key()}"},
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # Smoke test: create an unscheduled draft.
    print(create_draft("API connectivity test from brand-automation. Safe to delete."))
