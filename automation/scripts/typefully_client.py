#!/usr/bin/env python3
"""Minimal Typefully API v2 client.

Docs: https://typefully.com/docs/api
Auth: Authorization: Bearer <TYPEFULLY_API_KEY> (env or .env).
TYPEFULLY_SOCIAL_SET_ID pins the social set; auto-discovered when absent.
"""

import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from discord_notify import load_env  # noqa: E402

BASE = "https://api.typefully.com/v2"


def _headers():
    load_env()
    key = os.environ.get("TYPEFULLY_API_KEY")
    if not key:
        sys.exit("error: TYPEFULLY_API_KEY not set (env or .env)")
    return {"Authorization": f"Bearer {key}"}


def social_set_id() -> int:
    load_env()
    if os.environ.get("TYPEFULLY_SOCIAL_SET_ID"):
        return int(os.environ["TYPEFULLY_SOCIAL_SET_ID"])
    resp = requests.get(f"{BASE}/social-sets", headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()["results"][0]["id"]


def create_draft(
    thread: list[str] | None = None,
    linkedin: str | None = None,
    publish_at: str | None = None,
    title: str | None = None,
):
    """Create one draft targeting X (thread) and/or LinkedIn (single post).

    publish_at: ISO-8601 UTC datetime, "next-free-slot", "now", or None (draft).
    """
    platforms = {}
    if thread:
        platforms["x"] = {"posts": [{"text": t} for t in thread]}
    if linkedin:
        platforms["linkedin"] = {"posts": [{"text": linkedin}]}
    if not platforms:
        raise ValueError("nothing to post")
    payload = {"platforms": platforms}
    if publish_at:
        payload["publish_at"] = publish_at
    if title:
        payload["draft_title"] = title
    resp = requests.post(
        f"{BASE}/social-sets/{social_set_id()}/drafts",
        headers=_headers(), json=payload, timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"typefully {resp.status_code}: {resp.text[:300]}")
    return resp.json()


if __name__ == "__main__":
    # Smoke test: unscheduled X-only draft, safe to delete in the app.
    print(create_draft(thread=["API v2 connectivity test from brand-automation. Safe to delete."]))
