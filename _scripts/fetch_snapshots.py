#!/usr/bin/env python3
"""Fetch the Artificial Analysis free-tier snapshot into _scripts/data/snapshots/.

Calls the free language-models endpoint (200 models/page) and saves the raw
pages as aa_p1..pN.json plus pulled_at.txt (fetch timestamp marker). The
generator (_scripts/generate_llm_dashboard.py) reads these files, so the whole
pipeline is offline-reproducible once the snapshots are in the repo.

API:  base  https://artificialanalysis.ai/api/v2
      auth  x-api-key header (NOT Authorization: Bearer)
      free  GET /language/models/free?tier=free&intelligence_index_version=4.1&page=N
      free tier quota: 100 requests / 24h (fixed window)

Requires the ARTIFICIAL_ANALYSIS_API env var. Docs: https://artificialanalysis.ai/data-api/docs
"""
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SNAP_DIR = SCRIPT_DIR / "data" / "snapshots"
BASE = "https://artificialanalysis.ai/api/v2/language/models/free"
TIER = "free"
VERSION = "4.1"
MAX_PAGES = 8  # safety cap; pagination drives the real loop


def main() -> int:
    key = os.environ.get("ARTIFICIAL_ANALYSIS_API", "")
    if not key:
        print("ERROR: ARTIFICIAL_ANALYSIS_API env var not set", file=sys.stderr)
        return 1

    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    pages: list[Path] = []
    page = 1
    while page <= MAX_PAGES:
        url = f"{BASE}?tier={TIER}&intelligence_index_version={VERSION}&page={page}"
        req = urllib.request.Request(url, headers={"x-api-key": key})
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.load(resp)
            remaining = resp.headers.get("X-RateLimit-Remaining", "?")
        data = body.get("data") or []
        print(f"page {page}: {len(data)} models (quota left: {remaining})")
        out = SNAP_DIR / f"aa_p{page}.json"
        out.write_text(json.dumps(body, indent=1), "utf-8")
        pages.append(out)
        if not (body.get("pagination") or {}).get("has_more"):
            break
        page += 1
        time.sleep(1)  # be polite to the free tier

    marker = SNAP_DIR / "pulled_at.txt"
    marker.write_text(datetime.now(timezone.utc).isoformat() + "\n", "utf-8")
    total = sum(len(json.load(open(p))["data"]) for p in pages)
    print(f"saved {len(pages)} pages ({total} models) -> {SNAP_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())