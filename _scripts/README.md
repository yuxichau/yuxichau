# _scripts — LLM dashboard pipeline

Builds and refreshes the [LLM Intelligence vs Cost](/projects/llm-model-analysis/)
dashboard page (`_pages/llm-model-analysis.html`).

## Pipeline

```
fetch_snapshots.py  ->  _scripts/data/snapshots/aa_p1..N.json + pulled_at.txt
                              |
generate_llm_dashboard.py <-- snapshots + _scripts/vendor/chart.umd.js
                              |
                              +-> _pages/llm-model-analysis.html  (embedded data + Chart.js)
                              +-> _scripts/data/aa_top50_raw.json (top-50 audit snapshot)
```

- **`fetch_snapshots.py`** — calls the Artificial Analysis free-tier API
  (`https://artificialanalysis.ai/api/v2`, `x-api-key` header, 200 models/page,
  quota 100 req/24h) and stores the raw pages in the repo. Needs
  `ARTIFICIAL_ANALYSIS_API`.
- **`generate_llm_dashboard.py`** — offline, deterministic: takes the top 50
  models by Intelligence Index v4.1 from the vendored snapshots, inlines the
  vendored Chart.js bundle (v4.4.1) and the data into the page. No API calls.
- **`refresh_dashboard.sh`** — the one-command entry point: fetch → generate →
  commit → push → trigger the Cloudflare Pages build (via `deploy.sh`).
  Commits/deploys only when the generated output changed.
- **`deploy.sh`** — push to `main` + trigger the CF Pages build from the repo
  (records the commit hash in the deployment). See the yuxichau-blog skill.

## Vendored files (commit these, never delete)

| Path | What | Why |
| --- | --- | --- |
| `data/snapshots/aa_p*.json` | raw AA API pages (200/page) | offline regeneration + audit |
| `data/snapshots/pulled_at.txt` | fetch timestamp | the "Data pulled" date on the page |
| `data/aa_top50_raw.json` | top-50 raw snapshot | audit trail of what's displayed |
| `vendor/chart.umd.js` | Chart.js 4.4.1 UMD bundle | page is self-contained; no CDN dep |

Everything lives in the repo (no `/tmp`, no network) once the snapshots are
committed — a fresh checkout can regenerate the exact page.

## Commands

```bash
export ARTIFICIAL_ANALYSIS_API=<key>
export CLOUDFLARE_API_TOKEN=<token>

make refresh-dashboard   # fetch + generate + commit + push + deploy (if changed)
python3 _scripts/generate_llm_dashboard.py   # regenerate only, from committed snapshots
```

## Updating Chart.js

```bash
npm pack chart.js@4.4.1   # or: npm install --prefix /tmp/chartjs chart.js@4.4.1
cp /tmp/chartjs/node_modules/chart.js/dist/chart.umd.js _scripts/vendor/chart.umd.js
# verify the page still renders; commit the bumped bundle
```