#!/usr/bin/env bash
# Deploy yuxichau.com: push to main, then trigger the Cloudflare Pages build
# from the repo (records the exact commit hash in the deployment metadata).
#
# The CF git-integration webhook is currently MISSING (repo has no GitHub
# hooks), so pushes do not auto-build. Until the webhook is recreated
# (CF dashboard -> project -> Settings -> Builds & deployments ->
# "Connect to GitHub"), this API trigger is the official deploy step.
#
# Usage: CLOUDFLARE_API_TOKEN=<token> ./_scripts/deploy.sh
# Requires: git push working (SSH), CLOUDFLARE_API_TOKEN env var.

set -euo pipefail

ACCOUNT_ID="7310ba85833555ef21c11f387c8a9ef2"
PROJECT="yuxichau"
API_BASE="https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/pages/projects/${PROJECT}"

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  echo "ERROR: CLOUDFLARE_API_TOKEN is not set" >&2
  exit 1
fi

if ! git diff --quiet; then
  echo "WARNING: working tree is dirty. The deployed site will NOT match the committed tree."
  echo "         Commit or stash first for a clean, auditable deploy."
fi

echo "==> Pushing to origin/main"
git push origin main

echo "==> Triggering Cloudflare Pages build from main"
RESP=$(curl -s -X POST \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"branch":"main"}' \
  "${API_BASE}/deployments")

DEP_ID=$(python3 -c "import json,sys; d=json.load(sys.stdin); print((d.get('result') or {}).get('id',''))" <<<"$RESP")
if [[ -z "$DEP_ID" ]]; then
  echo "ERROR: trigger failed" >&2
  echo "$RESP" >&2
  exit 1
fi

echo "==> Deployment: https://${DEP_ID}.yuxichau.pages.dev (poll ${API_BASE}/deployments/${DEP_ID})"