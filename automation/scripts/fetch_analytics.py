#!/usr/bin/env python3
"""Pull last week's GA4 + Search Console data into one JSON blob.

Env (or .env): GA4_PROPERTY_ID, GA_SA_KEY (path to service-account JSON).
Output: JSON on stdout — traffic by channel/campaign/page/day + GSC queries.
GSC data lags ~2 days, so its window is offset accordingly.
"""

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

sys.path.insert(0, str(Path(__file__).parent))
from discord_notify import load_env  # noqa: E402

import os  # noqa: E402

SITE_URL = "sc-domain:mengyahu.com"


def token():
    creds = service_account.Credentials.from_service_account_file(
        os.environ["GA_SA_KEY"],
        scopes=["https://www.googleapis.com/auth/analytics.readonly",
                "https://www.googleapis.com/auth/webmasters.readonly"],
    )
    creds.refresh(Request())
    return creds.token


def ga4_report(tok, pid, dimensions, metrics, start, end, limit=50):
    resp = requests.post(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{pid}:runReport",
        headers={"Authorization": f"Bearer {tok}"},
        json={
            "dateRanges": [{"startDate": start, "endDate": end}],
            "dimensions": [{"name": d} for d in dimensions],
            "metrics": [{"name": m} for m in metrics],
            "limit": limit,
        }, timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    rows = []
    for r in data.get("rows", []):
        rows.append({
            **{dimensions[i]: v["value"] for i, v in enumerate(r.get("dimensionValues", []))},
            **{metrics[i]: v["value"] for i, v in enumerate(r.get("metricValues", []))},
        })
    return rows


def gsc_query(tok, dims, start, end, limit=25):
    resp = requests.post(
        f"https://searchconsole.googleapis.com/webmasters/v3/sites/{requests.utils.quote(SITE_URL, safe='')}/searchAnalytics/query",
        headers={"Authorization": f"Bearer {tok}"},
        json={"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": limit},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("rows", [])


def newsletter_stats():
    """Subscriber growth + per-issue email performance, from Resend.

    Two sources: the signup database on this box knows when each address
    confirmed or unsubscribed (growth), and Resend knows what happened to each
    message (delivery and opens). Shape is unchanged from the Kit era so the
    weekly-report prompt keeps working.
    """
    import sqlite3
    from collections import defaultdict

    key = os.environ.get("RESEND_API_KEY")
    if not key:
        return {}
    H = {"Authorization": f"Bearer {key}"}
    try:
        contacts = []
        for lang in ("zh", "en"):
            aud = os.environ.get(f"RESEND_{lang.upper()}_AUDIENCE")
            if not aud:
                continue
            data = requests.get(f"https://api.resend.com/audiences/{aud}/contacts",
                                headers=H, timeout=30).json().get("data", [])
            for c in data:
                contacts.append({**c, "lang": lang})

        # Per-issue performance: group the individual sends by subject.
        sent = requests.get("https://api.resend.com/emails", headers=H,
                            timeout=30).json().get("data", [])
        by_subject = defaultdict(lambda: {"recipients": 0, "delivered": 0, "opened": 0,
                                          "clicked": 0, "date": ""})
        for e in sent:
            row = by_subject[e.get("subject", "")]
            row["recipients"] += 1
            row["date"] = (e.get("created_at") or "")[:10]
            if e.get("last_event") in ("delivered", "opened", "clicked"):
                row["delivered"] += 1
            if e.get("last_event") == "opened":
                row["opened"] += 1
            if e.get("last_event") == "clicked":
                row["clicked"] += 1
        # Open/click tracking is deliberately off: it needs a tracking subdomain
        # and works by embedding an invisible pixel in every email. Report None
        # rather than 0.0, so a missing measurement is never read as "nobody
        # opened it".
        tracking = requests.get("https://api.resend.com/domains", headers=H, timeout=30).json()
        tracked = any(d.get("open_tracking") for d in tracking.get("data", []))
        emails = [{"date": v["date"], "subject": k, "recipients": v["recipients"],
                   "delivered": v["delivered"],
                   "open_rate": (round(v["opened"] / v["recipients"], 3)
                                 if tracked and v["recipients"] else None),
                   "click_rate": (round(v["clicked"] / v["recipients"], 3)
                                  if tracked and v["recipients"] else None)}
                  for k, v in by_subject.items()]
        emails.sort(key=lambda r: r["date"], reverse=True)

        states = {}
        db = Path("/home/mia/subscribe/subscribe.db")
        if db.exists():
            conn = sqlite3.connect(db)
            for email, lang, state, confirmed in conn.execute(
                    "SELECT email, lang, state, confirmed FROM subscribers"):
                states[(email, lang)] = (state, confirmed)
            conn.close()

        active = [c for c in contacts if not c.get("unsubscribed")]
        return {
            "subscribers_total_active": len(active),
            "subscribers_by_date": sorted(
                [{"email_masked": c["email"][:3] + "***", "lang": c["lang"],
                  "state": "unsubscribed" if c.get("unsubscribed") else "active",
                  "since": (c.get("created_at") or "")[:10]} for c in contacts],
                key=lambda r: r["since"]),
            "unsubscribed_total": sum(1 for s, _ in states.values() if s == "unsubscribed"),
            "pending_unconfirmed": sum(1 for s, _ in states.values() if s == "pending"),
            "recent_emails": emails[:12],
            "open_tracking": tracked,
            "tracking_note": ("开信率未追踪（Resend 开信追踪需要隐形像素，已按隐私取向关闭）；"
                              "邮件效果只看送达数，读者行为看 GA4 的 newsletter UTM"),
        }
    except Exception as exc:
        return {"error": str(exc)[:200]}


def main():
    load_env()
    pid = os.environ["GA4_PROPERTY_ID"]
    tok = token()
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=6)
    s, e = start.isoformat(), end.isoformat()
    gsc_end = date.today() - timedelta(days=3)
    gsc_start = gsc_end - timedelta(days=6)

    out = {
        "window": {"start": s, "end": e},
        "by_channel": ga4_report(tok, pid, ["sessionSource", "sessionMedium"],
                                 ["sessions", "totalUsers"], s, e),
        "by_campaign": ga4_report(tok, pid, ["sessionCampaignName"],
                                  ["sessions"], s, e),
        "by_page": ga4_report(tok, pid, ["pagePath"],
                              ["screenPageViews", "activeUsers", "userEngagementDuration"], s, e),
        "by_day": ga4_report(tok, pid, ["date"], ["sessions", "activeUsers"], s, e),
        "gsc_window": {"start": gsc_start.isoformat(), "end": gsc_end.isoformat()},
        "gsc_queries": gsc_query(tok, ["query"], gsc_start.isoformat(), gsc_end.isoformat()),
        "gsc_pages": gsc_query(tok, ["page"], gsc_start.isoformat(), gsc_end.isoformat()),
    }
    out["newsletter"] = newsletter_stats()
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
