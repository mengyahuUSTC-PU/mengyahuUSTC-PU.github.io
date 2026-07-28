#!/usr/bin/env bash
# Monday weekly report: pull analytics -> claude analysis -> save + email.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"
DATE=$(TZ=America/Los_Angeles date +%F)
PY=${PYTHON_BIN:-automation/.venv/bin/python}
REPORTS=automation/reports
mkdir -p "$REPORTS"

DATA=$("$PY" automation/scripts/fetch_analytics.py)
PREV=$(ls -1 "$REPORTS"/*.md 2>/dev/null | tail -1 || true)
POSTS=$(ls -1 src/content/blog/zh/*.md | xargs -n1 basename)

{
  cat automation/prompts/editorial-baseline.md automation/prompts/weekly-report.md
  echo "## 本周数据 JSON"
  echo "$DATA"
  echo "## 已发布文章列表"
  echo "$POSTS"
  echo "## 分发发布记录（scheduled_for.at=下发时刻，x/linkedin=实际发出时刻，均 UTC；发出与下发相差≤3 分钟＝晚间即时发，否则＝高峰时段定时发）"
  "$PY" -c "
import json, glob
for f in sorted(glob.glob('automation/data/dist/*.json')):
    d = json.load(open(f))
    print(json.dumps({'slug': d.get('slug'), 'status': d.get('status'), 'scheduled_for': d.get('scheduled_for')}, ensure_ascii=False))
"
  if [ -n "$PREV" ]; then
    echo "## 上一期周报全文"
    cat "$PREV"
  fi
} | claude -p --output-format text --model fable --fallback-model opus \
  | "$PY" automation/scripts/split_output.py json > "$REPORTS/$DATE.md"

git add "$REPORTS/$DATE.md"
git -c user.name="$(git config user.name)" commit -q -m "Weekly report $DATE" || true
git push -q origin master || true

"$PY" automation/scripts/send_email.py "📊 博客周报 $DATE" "$REPORTS/$DATE.md"
"$PY" automation/scripts/discord_notify.py "📊 本周周报已生成并发送邮箱：$DATE（repo: automation/reports/$DATE.md）"
