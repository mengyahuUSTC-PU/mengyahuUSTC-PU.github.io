#!/usr/bin/env bash
# Generate a Chinese deep-dive draft for one selected candidate.
# Usage: generate_deep_dive.sh [YYYY-MM-DD] [rank]
#   date defaults to today (UTC), rank defaults to 1 (top candidate).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

DATE=${1:-$(date -u +%F)}
RANK=${2:-1}
PROMPTS=automation/prompts
DATA=automation/data
DRAFTS=automation/drafts
PY=${PYTHON_BIN:-automation/.venv/bin/python}

SELECTION="$DATA/selection-$DATE.json"
[ -s "$SELECTION" ] || { echo "error: $SELECTION not found (run run_daily.sh first)"; exit 1; }

TOPIC=$("$PY" -c "
import json
cands = json.load(open('$SELECTION'))['deep_dive_candidates']
pick = [c for c in cands if c.get('rank') == $RANK] or [cands[$RANK - 1]]
print(json.dumps(pick[0], ensure_ascii=False, indent=2))
")

echo "=== deep dive (rank $RANK) ==="
echo "$TOPIC"

OUT="$DRAFTS/deep-dive-$DATE-rank$RANK.zh.md"
cat "$PROMPTS/editorial-baseline.md" "$PROMPTS/deep-dive.md" \
  <(echo "## 今日日期：$DATE") \
  <(echo "## 选定选题 JSON") \
  <(echo "$TOPIC") \
  | claude -p --output-format text > "$OUT"

echo "wrote $OUT"
