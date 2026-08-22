#!/usr/bin/env bash
# One-command dashboard refresh: fetch -> generate -> commit+push+deploy if changed.
#
# Usage: ARTIFICIAL_ANALYSIS_API=<key> CLOUDFLARE_API_TOKEN=<token> make refresh-dashboard
#   (or run ./_scripts/refresh_dashboard.sh with both env vars set)
#
# Commits only when the generated output actually changed, so weekly runs with
# no data movement produce no commits and no deploys.

set -euo pipefail
cd "$(dirname "$0")/.."   # repo root

echo "==> Fetching AA snapshot"
python3 _scripts/fetch_snapshots.py

echo "==> Regenerating dashboard page"
python3 _scripts/generate_llm_dashboard.py

git add _pages/llm-model-analysis.html \
        _scripts/data/aa_top50_raw.json \
        _scripts/data/snapshots/aa_p*.json \
        _scripts/data/snapshots/pulled_at.txt

if git diff --cached --quiet; then
  echo "Dashboard unchanged; nothing to commit or deploy."
  exit 0
fi

git commit -m "Refresh LLM dashboard data ($(date -u +%F))"
echo "==> Deploying"
CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:?set CLOUDFLARE_API_TOKEN}" bash _scripts/deploy.sh