#!/usr/bin/env bash
# Monthly review, run from cron on the 1st. Until 2026-10 the 1st only sent
# a Discord reminder, and the review happened only if the owner came asking;
# in September it never did. Now the review writes itself: refresh the
# topic memo the selector reads, pull 30 days of data, write the review,
# send it by email and Discord. Changes to the site or pipeline still go
# through Claude Code when the owner says 「做月度优化」.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"
MONTH=$(TZ=America/Los_Angeles date -d "yesterday" +%Y-%m)
PY=${PYTHON_BIN:-automation/.venv/bin/python}
REPORTS=automation/reports
mkdir -p "$REPORTS"
# DRY_RUN=1: write the review to /tmp only; no commit, email or Discord.
OUT="$REPORTS/monthly-$MONTH.md"
[ "${DRY_RUN:-0}" = "1" ] && OUT=/tmp/monthly-review-dry.md

"$PY" automation/scripts/topic_performance.py || true
DATA=$("$PY" automation/scripts/fetch_analytics.py --days 30)
PREV=$(ls -1 "$REPORTS"/monthly-*.md 2>/dev/null | tail -1 || true)

{
  cat automation/prompts/editorial-baseline.md automation/prompts/monthly-review.md
  echo "## 近 30 天数据 JSON"
  echo "$DATA"
  echo "## 选题表现"
  cat automation/data/topic-performance.md 2>/dev/null || echo "（本月未能生成）"
  echo "## 本月发布的深度文章"
  grep -l "^pubDate: $MONTH" src/content/blog/zh/*.md 2>/dev/null | grep -v briefing | xargs -r -n1 basename || true
  echo "## 分发记录"
  "$PY" -c "
import json, glob
for f in sorted(glob.glob('automation/data/dist/*.json')):
    d = json.load(open(f))
    print(d.get('slug'), d.get('status'), (d.get('scheduled_for') or {}).get('at', '')[:10])
"
  echo "## 最近四期周报"
  for f in $(ls -1 "$REPORTS"/20*.md | tail -4); do cat "$f"; echo; done
  if [ -n "$PREV" ]; then
    echo "## 上一期月度复盘"
    cat "$PREV"
  fi
} | /home/mia/bin/claude-pipe -p --output-format text --model fable --fallback-model opus \
  | "$PY" automation/scripts/split_output.py json > "$OUT"
[ "${DRY_RUN:-0}" = "1" ] && { echo "dry run: $OUT"; exit 0; }

git add "$REPORTS/monthly-$MONTH.md"
git -c user.name="$(git config user.name)" commit -q -m "Monthly review $MONTH" || true
git push -q origin master || true

"$PY" automation/scripts/send_email.py "📈 博客月度复盘 $MONTH" "$REPORTS/monthly-$MONTH.md"
"$PY" automation/scripts/discord_notify.py "📈 $MONTH 月度复盘已发到邮箱（automation/reports/monthly-$MONTH.md）。想实施里面的建议，来 Claude Code 说「做月度优化」。"
