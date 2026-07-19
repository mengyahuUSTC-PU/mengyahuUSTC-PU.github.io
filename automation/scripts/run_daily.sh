#!/usr/bin/env bash
# Daily pipeline: fetch sources -> topic selection -> briefing draft (zh + en).
# Runs on the Azure VM from cron. Never publishes anything: output goes to
# automation/data/ and automation/drafts/, which are gitignored.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

DATE=$(date -u +%F)
SCRIPTS=automation/scripts
PROMPTS=automation/prompts
DATA=automation/data
DRAFTS=automation/drafts
PY=${PYTHON_BIN:-automation/.venv/bin/python}

mkdir -p "$DATA" "$DRAFTS"

echo "=== [$(date -u +%FT%TZ)] fetch ==="
"$PY" "$SCRIPTS/fetch_sources.py"

POOL="$DATA/pool-$DATE.json"
[ -s "$POOL" ] || { echo "error: pool file missing"; exit 1; }

echo "=== topic selection ==="
cat "$PROMPTS/editorial-baseline.md" "$PROMPTS/editorial-lessons.md" "$PROMPTS/topic-selection.md" \
  <(echo "## 当日条目池 JSON") "$POOL" \
  | claude -p --output-format text --model sonnet \
  | "$PY" "$SCRIPTS/split_output.py" json > "$DATA/selection-$DATE.json"

"$PY" -c "import json,sys; d=json.load(open('$DATA/selection-$DATE.json')); \
print(f\"briefing items: {len(d.get('briefing_items',[]))}, deep-dive candidates: {len(d.get('deep_dive_candidates',[]))}\")"

echo "=== briefing draft ==="
cat "$PROMPTS/editorial-baseline.md" "$PROMPTS/editorial-lessons.md" "$PROMPTS/briefing.md" \
  <(echo "## 今日日期：$DATE") \
  <(echo "## briefing_items JSON") \
  <("$PY" -c "import json; print(json.dumps(json.load(open('$DATA/selection-$DATE.json'))['briefing_items'], ensure_ascii=False, indent=2))") \
  | claude -p --output-format text --model fable --fallback-model opus \
  | "$PY" "$SCRIPTS/split_output.py" bilingual "$DRAFTS/briefing-$DATE"

# Review loop (phase 3): briefing goes out as a PR, topic list goes to Discord.
# Both steps are skipped gracefully until Discord/gh are configured.
if [ -f .env ] && grep -q "^DISCORD_WEBHOOK_URL=" .env; then
  echo "=== briefing PR + Discord ==="
  PR_URL=$("$PY" "$SCRIPTS/make_pr.py" "$DRAFTS/briefing-$DATE.zh.md" "$DRAFTS/briefing-$DATE.en.md" || true)
  "$PY" "$SCRIPTS/discord_notify.py" "📰 **$DATE 快讯草稿**已开 PR：${PR_URL:-（PR 创建失败，见 VM 日志）}
Merge = 发布上线。"
  "$PY" "$SCRIPTS/discord_notify.py" --topics "$DATE"
fi

echo "=== [$(date -u +%FT%TZ)] done ==="
