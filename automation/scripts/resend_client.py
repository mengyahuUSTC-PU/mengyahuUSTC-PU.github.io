#!/usr/bin/env python3
"""Newsletter sending via Resend, with the subscriber list still living in Kit.

Kit's free plan refuses POST /broadcasts (403 "insufficient permissions") but
its read endpoints work fine, so the split is: Kit keeps the signup forms and
stays the list of record, Resend does the actual sending from mia@mengyahu.com.

Env (repo .env): RESEND_API_KEY, plus the existing KIT_* ids.
Docs: https://resend.com/docs/api-reference/emails/send-batch-emails
"""

import hmac
import os
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import quote

import requests

API = "https://api.resend.com"
FROM = "Mia Hu <mia@mengyahu.com>"
REPLY_TO = "mia@mengyahu.com"
BATCH_LIMIT = 100  # Resend's per-request cap


class ResendError(RuntimeError):
    """Resend refused the send. Carries the response body, which says why."""


SUPPRESSION = Path(__file__).resolve().parents[1] / "data" / "unsubscribed.txt"


def suppressed() -> set[str]:
    """Addresses that must never be mailed again, kept locally.

    Kit is the list of record but the unsubscribe link in the email is a mailto
    the human actions by hand, so this file is the durable record: whatever
    happens in Kit, an address in here is never sent to.
    """
    if not SUPPRESSION.exists():
        return set()
    return {line.strip().lower() for line in SUPPRESSION.read_text().splitlines()
            if line.strip() and not line.startswith("#")}


def unsubscribe(email: str) -> str:
    """Honour an opt-out everywhere: suppression file first, then Resend."""
    email = email.strip().lower()
    SUPPRESSION.parent.mkdir(parents=True, exist_ok=True)
    if email not in suppressed():
        with SUPPRESSION.open("a") as fh:
            fh.write(email + "\n")

    key = os.environ["RESEND_API_KEY"]
    notes = []
    for lang in ("zh", "en"):
        aud = os.environ.get(f"RESEND_{lang.upper()}_AUDIENCE")
        if not aud:
            continue
        r = requests.patch(f"{API}/audiences/{aud}/contacts/{quote(email)}",
                           headers={"Authorization": f"Bearer {key}",
                                    "Content-Type": "application/json"},
                           json={"unsubscribed": True}, timeout=30)
        notes.append(f"{lang} {r.status_code}")
    return "已加入永久屏蔽名单，Resend " + " / ".join(notes)


def recipients(lang: str) -> list[str]:
    """Subscribed contacts of that language's Resend audience, minus suppressions.

    Resend is the list of record now: the signup endpoint at api.mengyahu.com
    writes confirmed addresses here, and the unsubscribe link flips the same
    contact to unsubscribed. The local suppression file stays as a backstop.
    """
    aud = os.environ[f"RESEND_{lang.upper()}_AUDIENCE"]
    key = os.environ["RESEND_API_KEY"]
    resp = requests.get(f"{API}/audiences/{aud}/contacts",
                        headers={"Authorization": f"Bearer {key}"}, timeout=30)
    resp.raise_for_status()
    blocked = suppressed()
    return sorted({c["email"] for c in resp.json().get("data", [])
                   if not c.get("unsubscribed")
                   and c["email"].lower() not in blocked})


def _unsubscribe_url(email: str, lang: str) -> str:
    """Signed so the link works without a lookup and cannot be forged."""
    secret = os.environ["SUBSCRIBE_SECRET"].encode()
    sig = hmac.new(secret, f"{email}|{lang}".encode(), sha256).hexdigest()[:32]
    return f"https://api.mengyahu.com/unsubscribe?e={quote(email)}&l={lang}&s={sig}"


def _footer(lang: str, email: str) -> str:
    """One click, no human in the loop."""
    url = _unsubscribe_url(email, lang)
    style = 'font-size:12px;color:#888'
    if lang == "zh":
        return (f'<hr><p style="{style}">订阅自 mengyahu.com · '
                f'<a href="{url}" style="color:#888">退订</a></p>')
    return (f'<hr><p style="{style}">Subscribed at mengyahu.com · '
            f'<a href="{url}" style="color:#888">Unsubscribe</a></p>')


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

    # One message per person: no shared To: header, and each carries its own
    # signed unsubscribe link in both the body and the header.
    messages = [{
        "from": FROM,
        "to": [address],
        "reply_to": REPLY_TO,
        "subject": subject,
        "html": html + _footer(lang, address),
        "headers": {
            "List-Unsubscribe": f"<{_unsubscribe_url(address, lang)}>",
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
