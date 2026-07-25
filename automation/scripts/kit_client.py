#!/usr/bin/env python3
"""Minimal Kit (ConvertKit) V4 API client for the newsletter pipeline.

Env (repo .env): KIT_API_KEY, KIT_ZH_TAG_ID, KIT_EN_TAG_ID,
KIT_ZH_FORM_ID, KIT_EN_FORM_ID. Docs: https://developers.kit.com
"""

import os
from datetime import datetime, timedelta, timezone

import requests

API = "https://api.kit.com/v4"


def _headers():
    return {"X-Kit-Api-Key": os.environ["KIT_API_KEY"]}


def _ids(lang: str):
    return (
        int(os.environ[f"KIT_{lang.upper()}_FORM_ID"]),
        int(os.environ[f"KIT_{lang.upper()}_TAG_ID"]),
    )


def _paged(path: str, key: str):
    cursor, out = None, []
    while True:
        params = {"per_page": 500}
        if cursor:
            params["after"] = cursor
        resp = requests.get(f"{API}{path}", headers=_headers(), params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        out += data[key]
        page = data.get("pagination") or {}
        if not page.get("has_next_page"):
            return out
        cursor = page["end_cursor"]


def sync_form_tag(lang: str) -> int:
    """Tag every subscriber of the lang form with the lang tag (idempotent).

    Broadcasts can only target tags/segments, not forms, so the tag is the
    source of truth for who receives each language's emails.
    """
    form_id, tag_id = _ids(lang)
    subs = _paged(f"/forms/{form_id}/subscribers", "subscribers")
    tagged = {s["id"] for s in _paged(f"/tags/{tag_id}/subscribers", "subscribers")}
    for sub in subs:
        if sub["id"] not in tagged:
            requests.post(
                f"{API}/tags/{tag_id}/subscribers/{sub['id']}",
                headers=_headers(), timeout=30,
            ).raise_for_status()
    return len(subs)


def send_broadcast(lang: str, subject: str, html: str, preview_text: str = "") -> int:
    """Create a broadcast to the lang tag, scheduled 2 minutes out.

    Returns the number of subscribers targeted; 0 means nothing was created.
    """
    count = sync_form_tag(lang)
    if count == 0:
        return 0
    _, tag_id = _ids(lang)
    send_at = (datetime.now(timezone.utc) + timedelta(minutes=2)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    resp = requests.post(
        f"{API}/broadcasts",
        headers={**_headers(), "Content-Type": "application/json"},
        json={
            "subject": subject,
            "content": html,
            "description": f"auto: {subject}",
            "preview_text": preview_text or subject,
            "public": False,
            "published_at": None,
            "send_at": send_at,
            "subscriber_filter": [
                {"all": [{"type": "tag", "ids": [tag_id]}], "any": None, "none": None}
            ],
        },
        timeout=30,
    )
    resp.raise_for_status()
    return count
