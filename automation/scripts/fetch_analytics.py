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
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
