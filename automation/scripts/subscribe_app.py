#!/usr/bin/env python3
"""Subscription endpoint for mengyahu.com, replacing Kit's hosted form.

The site is static, so it cannot hold an API key; this service is the only
thing that talks to Resend with credentials. It does the three jobs Kit used
to do, and does the two of them Kit was doing badly:

  * accept a signup without letting anyone stuff the list (honeypot + rate cap)
  * confirm the address actually belongs to the person (double opt-in)
  * unsubscribe in one click, no human in the loop

State lives in SQLite next to the service. Resend audiences are the list of
record for sending; this database is the audit trail and the token store.
"""

import hmac
import json
import os
import re
import sqlite3
import time
from hashlib import sha256
from pathlib import Path
from secrets import token_urlsafe
from urllib.parse import quote

import requests
from flask import Flask, Response, jsonify, redirect, request

DB = Path(os.environ.get("SUBSCRIBE_DB", "/home/mia/subscribe/subscribe.db"))
SECRET = os.environ["SUBSCRIBE_SECRET"].encode()
RESEND_KEY = os.environ["RESEND_API_KEY"]
AUDIENCES = {"zh": os.environ["RESEND_ZH_AUDIENCE"], "en": os.environ["RESEND_EN_AUDIENCE"]}
SITE = "https://mengyahu.com"
SUPPRESSION = Path("/home/mia/site/automation/data/unsubscribed.txt")
API = "https://api.mengyahu.com"
FROM = "Mia Hu <mia@mengyahu.com>"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

app = Flask(__name__)


def db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS subscribers (
        email TEXT NOT NULL, lang TEXT NOT NULL, state TEXT NOT NULL,
        token TEXT, created REAL, confirmed REAL, contact_id TEXT,
        PRIMARY KEY (email, lang))""")
    conn.execute("""CREATE TABLE IF NOT EXISTS hits (ip TEXT, at REAL)""")
    return conn


def rate_limited(ip: str, limit: int = 5, window: int = 3600) -> bool:
    conn = db()
    now = time.time()
    conn.execute("DELETE FROM hits WHERE at < ?", (now - window,))
    n = conn.execute("SELECT COUNT(*) FROM hits WHERE ip = ?", (ip,)).fetchone()[0]
    conn.execute("INSERT INTO hits VALUES (?, ?)", (ip, now))
    conn.commit()
    conn.close()
    return n >= limit


def sign(email: str, lang: str) -> str:
    """Unsubscribe links must work without a lookup and without being guessable."""
    return hmac.new(SECRET, f"{email}|{lang}".encode(), sha256).hexdigest()[:32]


def resend(method: str, path: str, **kw):
    return requests.request(
        method, f"https://api.resend.com{path}",
        headers={"Authorization": f"Bearer {RESEND_KEY}", "Content-Type": "application/json"},
        timeout=30, **kw)


def page(title: str, body: str, lang: str = "en") -> Response:
    """Small self-contained confirmation pages, styled like the site."""
    html = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>body{{background:#f7f4ed;color:#1c1a17;font-family:system-ui,-apple-system,"Helvetica Neue",sans-serif;
display:flex;min-height:100vh;margin:0;align-items:center;justify-content:center;padding:24px}}
main{{max-width:26rem;text-align:center}}h1{{font-size:1.35rem;margin:0 0 .6rem}}
p{{color:#6f675a;line-height:1.7;margin:0 0 1.4rem}}a{{color:#c2500f}}</style></head>
<body><main><h1>{title}</h1>{body}</main></body></html>"""
    return Response(html, mimetype="text/html")


@app.post("/subscribe")
def subscribe():
    data = request.form or request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    lang = data.get("lang") if data.get("lang") in AUDIENCES else "en"

    # Honeypot: a real person never fills a hidden field.
    if (data.get("website") or "").strip():
        return jsonify(ok=True), 200
    if not EMAIL_RE.match(email) or len(email) > 254:
        return jsonify(ok=False, error="invalid_email"), 400
    if rate_limited(request.headers.get("X-Forwarded-For", request.remote_addr or "?")):
        return jsonify(ok=False, error="rate_limited"), 429

    conn = db()
    row = conn.execute("SELECT state FROM subscribers WHERE email=? AND lang=?",
                       (email, lang)).fetchone()
    if row and row[0] == "confirmed":
        conn.close()
        return jsonify(ok=True, state="already"), 200

    token = token_urlsafe(24)
    conn.execute("""INSERT INTO subscribers (email, lang, state, token, created)
                    VALUES (?,?,'pending',?,?)
                    ON CONFLICT(email, lang) DO UPDATE SET token=excluded.token,
                    state='pending', created=excluded.created""",
                 (email, lang, token, time.time()))
    conn.commit()
    conn.close()

    link = f"{API}/confirm?token={token}"
    if lang == "zh":
        subject = "确认订阅 Mengya (Mia) Hu 的更新"
        body = (f'<p>点一下确认订阅，之后每篇深度文章上线我会发给你：</p>'
                f'<p><a href="{link}">确认订阅</a></p>'
                f'<p style="font-size:12px;color:#888">不是你本人操作的话，忽略这封信就好，'
                f'没点确认就不会收到任何东西。</p>')
    else:
        subject = "Confirm your subscription to Mengya (Mia) Hu"
        body = (f'<p>Click to confirm, and I will email you when a new deep dive goes up:</p>'
                f'<p><a href="{link}">Confirm subscription</a></p>'
                f'<p style="font-size:12px;color:#888">If this was not you, ignore this email. '
                f'Nothing happens until you confirm.</p>')

    resend("POST", "/emails", json={"from": FROM, "to": [email], "reply_to": "mia@mengyahu.com",
                                    "subject": subject, "html": body})
    return jsonify(ok=True, state="pending"), 200


@app.get("/confirm")
def confirm():
    token = request.args.get("token", "")
    conn = db()
    row = conn.execute("SELECT email, lang FROM subscribers WHERE token=? AND state='pending'",
                       (token,)).fetchone()
    if not row:
        conn.close()
        return page("This link has expired", '<p>Try subscribing again from '
                    f'<a href="{SITE}">mengyahu.com</a>.</p>'), 404

    email, lang = row
    # An explicit re-subscribe overrides an earlier opt-out, otherwise the
    # suppression list would silently swallow someone who deliberately came back.
    if SUPPRESSION.exists():
        kept = [ln for ln in SUPPRESSION.read_text().splitlines()
                if ln.strip().lower() != email]
        SUPPRESSION.write_text("\n".join(kept) + ("\n" if kept else ""))

    r = resend("POST", f"/audiences/{AUDIENCES[lang]}/contacts",
               json={"email": email, "unsubscribed": False})
    contact_id = (r.json() or {}).get("id") if r.status_code < 300 else None
    conn.execute("""UPDATE subscribers SET state='confirmed', confirmed=?, token=NULL,
                    contact_id=? WHERE email=? AND lang=?""",
                 (time.time(), contact_id, email, lang))
    conn.commit()
    conn.close()

    if lang == "zh":
        return page("订阅成功", f'<p>下一篇深度文章上线时你会收到邮件。'
                    f'每封信底部都有一键退订。</p><p><a href="{SITE}/zh/">回到网站</a></p>', "zh")
    return page("You are subscribed", f'<p>You will get an email when the next deep dive goes up. '
                f'Every email has one-click unsubscribe.</p><p><a href="{SITE}/en/">Back to the site</a></p>')


@app.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe():
    """GET is the link in the footer; POST is Gmail's one-click header."""
    email = (request.args.get("e") or "").strip().lower()
    lang = request.args.get("l") if request.args.get("l") in AUDIENCES else "en"
    if not hmac.compare_digest(request.args.get("s", ""), sign(email, lang)):
        return page("Link not valid", "<p>Reply to any of my emails and I will remove you by hand.</p>"), 400

    conn = db()
    conn.execute("UPDATE subscribers SET state='unsubscribed' WHERE email=? AND lang=?", (email, lang))
    conn.commit()
    conn.close()
    resend("PATCH", f"/audiences/{AUDIENCES[lang]}/contacts/{quote(email)}",
           json={"unsubscribed": True})

    # Same durable record the Discord command writes, so an opt-out survives
    # even if the Resend contact is ever recreated by an import.
    SUPPRESSION.parent.mkdir(parents=True, exist_ok=True)
    current = SUPPRESSION.read_text().splitlines() if SUPPRESSION.exists() else []
    if email not in {ln.strip().lower() for ln in current}:
        with SUPPRESSION.open("a") as fh:
            fh.write(email + "\n")

    if request.method == "POST":  # one-click: no page, just an ack
        return jsonify(ok=True), 200
    if lang == "zh":
        return page("已退订", "<p>不会再收到我的邮件了。想回来的话，网站上随时可以再订阅。</p>", "zh")
    return page("Unsubscribed", "<p>You will not get any more email from me. "
                "You can always subscribe again from the site.</p>")


@app.get("/health")
def health():
    conn = db()
    n = conn.execute("SELECT COUNT(*) FROM subscribers WHERE state='confirmed'").fetchone()[0]
    conn.close()
    return jsonify(ok=True, confirmed=n)
