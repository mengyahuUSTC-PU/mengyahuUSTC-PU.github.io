#!/usr/bin/env python3
"""Newsletter sending via Resend, with the subscriber list still living in Kit.

Kit's free plan refuses POST /broadcasts (403 "insufficient permissions") but
its read endpoints work fine, so the split is: Kit keeps the signup forms and
stays the list of record, Resend does the actual sending from mia@mengyahu.com.

Env (repo .env): RESEND_API_KEY, plus the existing KIT_* ids.
Docs: https://resend.com/docs/api-reference/emails/send-batch-emails
"""

import os
from html import escape

import requests

API = "https://api.resend.com"
FROM = "Mia Hu <mia@mengyahu.com>"
REPLY_TO = "mia@mengyahu.com"
BATCH_LIMIT = 100  # Resend's per-request cap


class ResendError(RuntimeError):
    """Resend refused the send. Carries the response body, which says why."""


def recipients(lang: str) -> list[str]:
    """Active subscribers carrying the language tag, read from Kit."""
    from kit_client import _headers, _paged, _ids  # reuse the existing client

    _, tag_id = _ids(lang)
    subs = _paged(f"/tags/{tag_id}/subscribers", "subscribers")
    return sorted({s["email_address"] for s in subs if s.get("state") == "active"})


def _footer(lang: str, subject: str) -> str:
    """Every email needs a working opt-out. At this list size that is a reply
    the human handles, so the mailto has to be real and the wording plain."""
    mailto = f"mailto:{REPLY_TO}?subject={escape('unsubscribe: ' + subject)}"
    style = 'font-size:12px;color:#888'
    if lang == "zh":
        return (f'<hr><p style="{style}">订阅自 mengyahu.com · '
                f'<a href="{mailto}" style="color:#888">退订</a></p>')
    return (f'<hr><p style="{style}">Subscribed at mengyahu.com · '
            f'<a href="{mailto}" style="color:#888">Unsubscribe</a></p>')


def send_newsletter(lang: str, subject: str, html: str) -> int:
    """Send one issue to every active subscriber of that language.

    Returns the number of recipients; 0 means nobody was subscribed and nothing
    was sent. Raises ResendError with the response body on failure.
    """
    to = recipients(lang)
    if not to:
        return 0

    key = os.environ.get("RESEND_API_KEY")
    if not key:
        raise ResendError("RESEND_API_KEY 没有设置（VM ~/site/.env）")

    body = html + _footer(lang, subject)
    unsubscribe = f"<mailto:{REPLY_TO}?subject=unsubscribe>"
    # One message per person: no shared To: header, so nobody sees the list.
    messages = [{
        "from": FROM,
        "to": [address],
        "reply_to": REPLY_TO,
        "subject": subject,
        "html": body,
        "headers": {
            "List-Unsubscribe": unsubscribe,
            "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
        },
    } for address in to]

    for chunk in (messages[i:i + BATCH_LIMIT] for i in range(0, len(messages), BATCH_LIMIT)):
        resp = requests.post(
            f"{API}/emails/batch",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=chunk,
            timeout=30,
        )
        if resp.status_code >= 300:
            raise ResendError(f"Resend {resp.status_code}: {resp.text[:300]}")
    return len(to)


def preflight() -> tuple[bool, str]:
    """Cheap check that the key works and the domain is verified, so a send
    never half-succeeds the way the Kit one did."""
    key = os.environ.get("RESEND_API_KEY")
    if not key:
        return False, "RESEND_API_KEY 未设置"
    resp = requests.get(f"{API}/domains", headers={"Authorization": f"Bearer {key}"}, timeout=30)
    if resp.status_code == 401 and "restricted" in resp.text:
        # A sending-only key cannot list domains. That is fine for sending, so
        # let the send itself be the test rather than blocking on the check.
        return True, "sending-only key（跳过域名检查）"
    if resp.status_code >= 300:
        return False, f"Resend {resp.status_code}: {resp.text[:200]}"
    domains = resp.json().get("data") or []
    mine = [d for d in domains if d.get("name") in ("mengyahu.com", "send.mengyahu.com")]
    if not mine:
        return False, "Resend 上还没有 mengyahu.com 这个域名"
    status = mine[0].get("status")
    if status != "verified":
        return False, f"域名 {mine[0]['name']} 状态是 {status}，还没验证通过"
    return True, f"{mine[0]['name']} verified"


if __name__ == "__main__":
    import sys
    if "--recipients" in sys.argv:
        for lang in ("zh", "en"):
            print(lang, recipients(lang))
    else:
        print(preflight())
