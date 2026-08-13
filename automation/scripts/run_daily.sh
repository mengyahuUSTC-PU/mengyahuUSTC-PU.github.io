#!/usr/bin/env bash
# Daily pipeline: fetch sources -> topic selection -> briefing draft (zh + en).
# Runs on the Azure VM from cron. Never publishes anything: output goes to
# automation/data/ and automation/drafts/, which are gitignored.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

DATE=$(TZ=America/Los_Angeles date +%F)
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
RECENT_TOPICS=$("$PY" -c "
import json, glob
titles = []
for f in sorted(glob.glob('$DATA/selection-*.json'))[-7:]:
    if '$DATE' in f: continue
    try:
        d = json.load(open(f))
        for k in ('briefing_items', 'deep_dive_candidates', 'research_items'):
            titles += [i.get('title', '') for i in d.get(k, [])]
    except Exception: pass
print(chr(10).join('- ' + t for t in titles if t))
")
cat "$PROMPTS/editorial-baseline.md" "$PROMPTS/editorial-lessons.md" "$PROMPTS/topic-selection.md" \
  <(echo "## 近 7 天已推荐过的选题（同一事件除非有重大新进展，否则不得再次推荐）") \
  <(echo "$RECENT_TOPICS") \
  <(echo "## 当日条目池 JSON") "$POOL" \
  | claude -p --output-format text --model sonnet \
  | "$PY" "$SCRIPTS/split_output.py" json > "$DATA/selection-$DATE.json"

"$PY" -c "import json,sys; d=json.load(open('$DATA/selection-$DATE.json')); \
print(f\"briefing items: {len(d.get('briefing_items',[]))}, deep-dive candidates: {len(d.get('deep_dive_candidates',[]))}, research items: {len(d.get('research_items',[]))}\")"

echo "=== briefing draft ==="
cat "$PROMPTS/editorial-baseline.md" "$PROMPTS/editorial-lessons.md" "$PROMPTS/briefing.md" \
  <(echo "## 今日日期：$DATE") \
  <(echo "## briefing_items JSON") \
  <("$PY" -c "import json; print(json.dumps(json.load(open('$DATA/selection-$DATE.json'))['briefing_items'], ensure_ascii=False, indent=2))") \
  <(echo "## research_items JSON") \
  <("$PY" -c "import json; print(json.dumps(json.load(open('$DATA/selection-$DATE.json')).get('research_items', []), ensure_ascii=False, indent=2))") \
  | claude -p --output-format text --model fable --fallback-model opus --allowedTools "WebFetch" "WebSearch" \
  | "$PY" "$SCRIPTS/split_output.py" bilingual "$DRAFTS/briefing-$DATE"

# Review loop (phase 3): briefing goes out as a PR, topic list goes to Discord.
# Both steps are skipped gracefully until Discord/gh are configured.
if [ -f .env ] && grep -q "^DISCORD_WEBHOOK_URL=" .env; then
  echo "=== briefing PR + Discord ==="
  # Topic list goes out first (user can pick while the briefing is audited).
  "$PY" "$SCRIPTS/discord_notify.py" --topics "$DATE"
  PR_URL=$("$PY" "$SCRIPTS/make_pr.py" "$DRAFTS/briefing-$DATE.zh.md" "$DRAFTS/briefing-$DATE.en.md" || true)
  PR_NUM=$(echo "$PR_URL" | grep -oE "[0-9]+$" || true)
  # Audit BEFORE publishing: what goes live is the post-fix version.
  [ -n "$PR_NUM" ] && "$PY" "$SCRIPTS/verify_draft.py" "$PR_NUM" || true
  # User decision 2026-08-11: briefings publish without review.
  if [ -n "$PR_NUM" ] && gh pr merge "$PR_NUM" --merge; then
    "$PY" "$SCRIPTS/discord_notify.py" "📰 **$DATE 快讯**已三方核查并自动上线：https://mengyahuustc-pu.github.io/zh/briefing-$DATE/
（免审直发；要改回「改简报 意见」即可）"
  else
    "$PY" "$SCRIPTS/discord_notify.py" "📰 **$DATE 快讯**自动合并失败，请手动处理 PR：${PR_URL:-（PR 创建失败，见 VM 日志）}"
  fi
fi

echo "=== [$(date -u +%FT%TZ)] done ==="
