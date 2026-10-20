#!/usr/bin/env python3
"""Which kinds of topics readers actually read, for the topic selector.

Writes automation/data/topic-performance.md, which run_daily appends to the
selection prompt. Refreshed on the 1st of each month by monthly_review.sh;
run it by hand any time. Before this the selector carried a fixed paragraph
of 2026-08-11 numbers; the October review found the most-written category
(agents and security, 16 of 51 essays) had the fewest readers per essay,
so the selector needs numbers that move with the site.

Readers = page_view users on the zh and en pages of each essay over the
last 90 days, Singapore excluded (headless crawlers, see fetch_analytics).
Finished = share of those readers who reached the 90% scroll mark.
"""

import glob
import os
import re
import statistics as st
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "automation" / "scripts"))
from discord_notify import load_env  # noqa: E402
from fetch_analytics import requests, token  # noqa: E402

OUT = REPO_ROOT / "automation" / "data" / "topic-performance.md"
BUCKETS = [  # first match wins; matched against slug, tags and English title
    ("工作与收入", r"job|labor|work(er|place)?\b|occupation|employ|hiring|layoff|salar|econom|financ|money|debt|pric"),
    ("隐私、健康与日常生活", r"privacy|health|hipaa|medic|tracker|surveil|cookie|broker|baby|teen|\bcar|consumer|child|age-gate|trip|travel|hik"),
    ("政策、法律与行业格局", r"polic|regulat|governance|\blaw|liabil|sanction|settlement|copyright|court|pace|veto|white-house|congress|lawsuit|dispute|priority|act\b"),
    ("agent 与安全攻防", r"agent|coding|prompt-injection|secur|cyber|token|attack|jailbreak|guardrail|red-team|vulnerab|crypto|worm|approval|theft"),
    ("模型与研究", r"model|benchmark|open-weight|watermark|align|welfare|\bcot\b|reasoning|research|math|proof|paper"),
]


def bucket(text):
    return next((name for name, rx in BUCKETS if re.search(rx, text, re.I)), "其他")


def ga(tok, pid, dims, mets, start, end):
    body = {"dateRanges": [{"startDate": start, "endDate": end}],
            "dimensions": [{"name": d} for d in dims], "metrics": [{"name": m} for m in mets],
            "limit": 5000,
            "dimensionFilter": {"notExpression": {"filter": {
                "fieldName": "country", "stringFilter": {"value": "Singapore"}}}}}
    r = requests.post(f"https://analyticsdata.googleapis.com/v1beta/properties/{pid}:runReport",
                      headers={"Authorization": f"Bearer {tok}"}, json=body, timeout=90)
    r.raise_for_status()
    return [[v["value"] for v in row["dimensionValues"]] + [v["value"] for v in row["metricValues"]]
            for row in r.json().get("rows", [])]


def front(path):
    text = Path(path).read_text()
    fm, body = text.split("---", 2)[1], text.split("---", 2)[2]
    get = lambda k: (re.search(rf"^{k}:\s*(.*)$", fm, re.M) or [None, ""])[1].strip().strip('"')
    return get, body


def main():
    load_env()
    tok, pid = token(), os.environ["GA4_PROPERTY_ID"]
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=89)
    users = defaultdict(lambda: defaultdict(int))
    for path, event, n in ga(tok, pid, ["pagePath", "eventName"], ["totalUsers"], start.isoformat(), end.isoformat()):
        m = re.match(r"^/(?:zh|en)/([^/]+)/?$", path)
        if m and event in ("page_view", "scroll"):
            users[m.group(1)][event] += int(n)

    rows = []
    for f in sorted(glob.glob(str(REPO_ROOT / "src/content/blog/zh/*.md"))):
        slug = Path(f).stem
        if slug.startswith("briefing") or slug == "hello-world":
            continue
        get, body = front(f)
        pub = get("pubDate")[:10]
        if not pub or pub > (end - timedelta(days=7)).isoformat() or pub < start.isoformat():
            continue  # too fresh to judge, or outside the window
        en = REPO_ROOT / "src/content/blog/en" / f"{slug}.md"
        en_title = front(en)[0]("title") if en.exists() else ""
        paras = [p for p in body.split("\n\n") if p.strip() and not p.lstrip().startswith("#")]
        rows.append({
            "slug": slug, "title": get("title"), "pub": pub,
            "bucket": bucket(" ".join([slug, get("tags"), en_title])),
            "readers": users[slug]["page_view"], "finished": users[slug]["scroll"],
            "personal": bool(re.search(r"我(自己|在|做|曾|当时|去|让|用|的(经历|项目|工作))", " ".join(paras[:3]))),
        })
    if len(rows) < 5:
        print("not enough essays in the window; memo left unchanged")
        return

    rate = lambda rs: sum(r["finished"] for r in rs) / max(1, sum(r["readers"] for r in rs))
    lines = [f"# 选题表现（自动生成 {date.today()}，{start}～{end} 近 90 天，已剔除疑似机器人流量）", "",
             "读者 = 中英两版页面的阅读人数之和；读完 = 读到 90% 位置的人占比。数据量小，看方向，不看小数点。", "",
             "| 类别 | 篇数 | 每篇读者（中位数） | 读完 |", "|---|---|---|---|"]
    by = defaultdict(list)
    for r in rows:
        by[r["bucket"]].append(r)
    for name, rs in sorted(by.items(), key=lambda kv: -st.median(r["readers"] for r in kv[1])):
        lines.append(f"| {name} | {len(rs)} | {st.median(r['readers'] for r in rs):.0f} | {rate(rs):.0%} |")
    top = sorted(rows, key=lambda r: -r["readers"])
    lines += ["", "读者最多：" + "；".join(f"《{r['title']}》{r['readers']}" for r in top[:5]),
              "读者最少：" + "；".join(f"《{r['title']}》{r['readers']}" for r in top[-5:])]
    p_yes, p_no = [r for r in rows if r["personal"]], [r for r in rows if not r["personal"]]
    if len(p_yes) >= 3:
        lines.append(f"开头有作者亲身经历的 {len(p_yes)} 篇读完率 {rate(p_yes):.0%}，其余 {len(p_no)} 篇 {rate(p_no):.0%}。")
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({len(rows)} essays)")


if __name__ == "__main__":
    main()
