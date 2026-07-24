#!/usr/bin/env bash
# Generate a Chinese deep-dive draft for one selected candidate.
# Usage: generate_deep_dive.sh [YYYY-MM-DD] [rank]
#   date defaults to today (UTC), rank defaults to 1 (top candidate).
#        generate_deep_dive.sh --topic "<free-form topic, links welcome>"
#   writes the draft for a user-supplied topic outside the daily candidate pool.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

SCRIPTS=automation/scripts
PROMPTS=automation/prompts
DATA=automation/data
DRAFTS=automation/drafts
PY=${PYTHON_BIN:-automation/.venv/bin/python}

if [ "${1:-}" = "--topic" ]; then
  [ -n "${2:-}" ] || { echo "error: --topic requires the topic text"; exit 1; }
  DATE=$(TZ=America/Los_Angeles date +%F)
  TOPIC=$("$PY" -c "
import json, sys
print(json.dumps({
    'title': sys.argv[1],
    'source': '用户手动指定（不在当日候选池）',
    'why': '用户主动提出想写这个话题。话题描述可能只是一句话或一个链接：'
           '先用 WebSearch/WebFetch 找到并通读一手来源（官方公告、论文、原始博客），'
           '核实事实后再动笔；若查证后发现事实与话题描述不符，以查证结果为准并在文中说明。',
}, ensure_ascii=False, indent=2))
" "$2")
  OUT="$DRAFTS/deep-dive-$DATE-custom-$(date +%H%M%S).zh.md"
  echo "=== deep dive (custom topic) ==="
else
  DATE=${1:-$(TZ=America/Los_Angeles date +%F)}
  RANK=${2:-1}

  SELECTION="$DATA/selection-$DATE.json"
  [ -s "$SELECTION" ] || { echo "error: $SELECTION not found (run run_daily.sh first)"; exit 1; }

  TOPIC=$("$PY" -c "
import json
cands = json.load(open('$SELECTION'))['deep_dive_candidates']
pick = [c for c in cands if c.get('rank') == $RANK] or [cands[$RANK - 1]]
print(json.dumps(pick[0], ensure_ascii=False, indent=2))
")
  OUT="$DRAFTS/deep-dive-$DATE-rank$RANK.zh.md"
  echo "=== deep dive (rank $RANK) ==="
fi

echo "$TOPIC"

cat "$PROMPTS/editorial-baseline.md" "$PROMPTS/editorial-lessons.md" "$PROMPTS/deep-dive.md" \
  <(echo "## 今日日期：$DATE") \
  <(echo "## 选定选题 JSON") \
  <(echo "$TOPIC") \
  | claude -p --output-format text --model fable --fallback-model opus --allowedTools "WebFetch" "WebSearch" \
  | "$PY" "$SCRIPTS/split_output.py" json > "$OUT"

echo "wrote $OUT"
