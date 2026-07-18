#!/usr/bin/env python3
"""Send an email via Gmail SMTP (app password).

Usage:
  send_email.py "Subject" body.md      # body from file
  send_email.py "Subject" - < body    # body from stdin

Env (or .env at repo root): GMAIL_ADDRESS, GMAIL_APP_PASSWORD,
REPORT_EMAIL (recipient, defaults to GMAIL_ADDRESS).
"""

import os
import smtplib
import sys
from email.mime.text import MIMEText
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from discord_notify import load_env  # noqa: E402


def main():
    load_env()
    sender = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not sender or not password:
        sys.exit("error: GMAIL_ADDRESS / GMAIL_APP_PASSWORD not set")
    recipient = os.environ.get("REPORT_EMAIL", sender)

    subject = sys.argv[1]
    source = sys.argv[2]
    body = sys.stdin.read() if source == "-" else Path(source).read_text()

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
    print(f"sent to {recipient}")


if __name__ == "__main__":
    main()
