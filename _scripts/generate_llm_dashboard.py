#!/usr/bin/env python3
"""Generate the LLM Intelligence vs Cost dashboard page for yuxichau.com.

Reads the Artificial Analysis free-tier API snapshots (saved in this repo under
_scripts/data/snapshots/aa_p*.json), takes the top 50 models by Intelligence
Index (v4.1), and writes:
  - _pages/llm-model-analysis.html   (the dashboard page, embedded data)
  - _scripts/data/aa_top50_raw.json  (top-50 raw snapshot for audit)

All inputs are repo-relative, so the pipeline runs from any checkout:
  generate:    python3 _scripts/generate_llm_dashboard.py
  full refresh: bash _scripts/refresh_dashboard.sh   (fetch -> generate -> deploy)
The Chart.js bundle (v4.4.1, vendored at _scripts/vendor/chart.umd.js) is
inlined into the page for self-containment. See _scripts/README.md.
"""
import json
import re
import os
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
SNAPS = [SCRIPT_DIR / "data" / "snapshots" / f"aa_p{i}.json" for i in range(1, 5)]
PAGE = REPO / "_pages/llm-model-analysis.html"
RAW = SCRIPT_DIR / "data" / "aa_top50_raw.json"
CHARTJS = SCRIPT_DIR / "vendor" / "chart.umd.js"  # v4.4.1, inlined for self-containment
PULLED_MARKER = SCRIPT_DIR / "data" / "snapshots" / "pulled_at.txt"

EFFORT_RANK = {"max": 0, "xhigh": 1, "high": 2, "medium": 3, "low": 4, "minimal": 5}

def pulled_date() -> str:
    """Date the current snapshot was fetched (from the fetch marker, else the
    existing raw snapshot's pulled_at, else today)."""
    try:
        txt = PULLED_MARKER.read_text().strip()
        if txt:
            return txt[:10]
    except OSError:
        pass
    try:
        with open(RAW) as f:
            return (json.load(f).get("pulled_at") or "")[:10]
    except (OSError, json.JSONDecodeError):
        pass
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def effort_of(name: str):
    m = re.search(r"\((.*?)\)", name)
    if not m:
        if "Max" in name:  # e.g. Qwen3.8 Max
            return "max"
        return None
    inner = m.group(1).lower()
    for eff in ["max", "xhigh", "high", "medium", "low", "minimal"]:
        if eff in inner:
            return eff
    return None

def reasoning_of(name: str):
    n = name.lower()
    if "adaptive reasoning" in n:
        return "Adaptive"
    if "non-reasoning" in n:
        return "Non-reasoning"
    if "reasoning" in n:
        return "Reasoning"
    if effort_of(name):
        return "Reasoning"  # effort configs imply a reasoning variant
    return "Standard"

def family_of(name: str):
    for f in ["Claude", "Gemini", "GPT", "Grok", "Qwen", "DeepSeek", "Kimi",
              "GLM", "MiniMax", "Motif", "Muse"]:
        if name.startswith(f) or f in name.split()[0]:
            return f
    return "Other"

# Licensing classification. Defaults by lab, corrected per model where the
# lab's usual practice does not apply (verified Aug 2026):
#   - Alibaba Qwen3.8 Max / Qwen3.8 2.4T: open weights landed ~Aug 12-14 2026
#     (2.4T under a custom license, 27B Apache 2.0) after an API-first launch.
#   - Alibaba Qwen3.7 Max: stayed API-only (every prior Max-tier Qwen is closed).
#   - Meta Muse Spark 1.x: weights announced Aug 10 2026 but not yet published
#     at the snapshot date; Muse Glimmer (not in the top 50) is Apache 2.0.
#   - Motif 3 (Beta): Artificial Analysis classifies it as proprietary (weights
#     not publicly available); an HF "Motif-3" repo exists but the AA-listed
#     beta is the model ranked here. Revisit at the GA release.
#   - Kimi K3: open weights under the custom Kimi K3 License (not OSI-approved,
#     counted here as open source per common usage).
#   - DeepSeek V4 (MIT), GLM-5.x (Z AI), MiniMax-M3: open weights.
CREATOR_LICENSE = {
    "Anthropic": "Proprietary",
    "OpenAI": "Proprietary",
    "SpaceXAI": "Proprietary",
    "Meta": "Proprietary",
    "Motif Technologies": "Proprietary",
    "Alibaba": "Open source",
    "DeepSeek": "Open source",
    "Z AI": "Open source",
    "Kimi": "Open source",
    "MiniMax": "Open source",
}
LICENSE_OVERRIDES = {
    "Qwen3.7 Max": "Proprietary",  # API-only; see notes above
}

def license_of(name: str, creator: str):
    base = name.split(" (")[0]
    return LICENSE_OVERRIDES.get(base, CREATOR_LICENSE.get(creator, "Proprietary"))

def load():
    models = []
    for p in SNAPS:
        with open(p) as f:
            models.extend(json.load(f)["data"])
    return models

def cost_of(m):
    c = m.get("artificial_analysis_intelligence_index_cost")
    if c and c.get("cost_per_task") and c["cost_per_task"].get("total_cost") is not None:
        return c["cost_per_task"]["total_cost"]
    return None

def main():
    models = load()
    def ii(m):
        return (m.get("evaluations") or {}).get("artificial_analysis_intelligence_index")
    with_ii = [m for m in models if ii(m) is not None]
    top = sorted(with_ii, key=lambda m: -ii(m))[:50]

    rows = []
    for rank, m in enumerate(top, 1):
        ev = m.get("evaluations") or {}
        pr = m.get("pricing") or {}
        pe = m.get("performance") or {}
        name = m["name"]
        creator = m["model_creator"]["name"]
        rows.append({
            "rank": rank,
            "name": name,
            "creator": creator,
            "license": license_of(name, creator),
            "family": family_of(name),
            "reasoning": reasoning_of(name),
            "effort": effort_of(name),
            "ii": ev.get("artificial_analysis_intelligence_index"),
            "coding": ev.get("artificial_analysis_coding_index"),
            "cost": cost_of(m),
            "price_in": pr.get("price_1m_input_tokens"),
            "price_out": pr.get("price_1m_output_tokens"),
            "tok_s": pe.get("median_output_tokens_per_second"),
            "ttft": pe.get("median_time_to_first_token_seconds"),
            "release": m.get("release_date"),
        })

    # preserve raw snapshot for audit
    os.makedirs(os.path.dirname(RAW), exist_ok=True)
    with open(RAW, "w") as f:
        json.dump({"pulled_at": datetime.now(timezone.utc).isoformat(),
                   "intelligence_index_version": "4.1",
                   "top_50": [m for m in top]}, f, indent=1)

    data_json = json.dumps(rows)
    pulled = pulled_date()
    with open(CHARTJS) as f:
        chartjs = f.read()
    # drop the sourceMappingURL trailer; the map isn't served, avoids a console 404
    chartjs = chartjs.split("//# sourceMappingURL=")[0].rstrip()
    page = (TEMPLATE
            .replace("__DATA__", data_json)
            .replace("__PULLED__", pulled)
            .replace("__CHARTJS__", chartjs))
    os.makedirs(os.path.dirname(PAGE), exist_ok=True)
    with open(PAGE, "w") as f:
        f.write(page)
    print(f"wrote {PAGE} ({len(rows)} models, {sum(1 for r in rows if r['cost'] is not None)} with cost)")

TEMPLATE = r'''---
layout: single
title: "LLM Intelligence vs Cost"
classes: wide
author_profile: false
permalink: /projects/llm-model-analysis/
---

<div class="llm-dash" id="llm-dash">

<style>
:root#llm-dash { }
#llm-dash {
  --bg: #ffffff; --card: #f6f8fa; --border: #d0d7de; --border-hover: #0969da;
  --text: #1f2328; --muted: #57606a; --accent: #0969da; --accent-bg: #ddf4ff;
  --good: #1a7f37; --good-bg: #dafbe1; --warn: #9a6700; --warn-bg: #fff8c5;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
  color: var(--text); line-height: 1.5;
}
#llm-dash .dash-header h1 { font-size: 1.8rem; margin: 0 0 .2rem; }
#llm-dash .dash-sub { color: var(--muted); margin: 0 0 1rem; font-size: .95rem; }
#llm-dash .dash-sub a { color: var(--accent); }
#llm-dash .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: .75rem; margin-bottom: 1.25rem; }
#llm-dash .kpi { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: .7rem .9rem; }
#llm-dash .kpi .k-label { font-size: .72rem; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); }
#llm-dash .kpi .k-value { font-size: 1.15rem; font-weight: 600; margin-top: .15rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
#llm-dash .kpi .k-note { font-size: .78rem; color: var(--muted); }
#llm-dash .filters { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: .8rem .9rem; margin-bottom: 1.25rem; display: flex; flex-wrap: wrap; gap: .9rem 1.4rem; align-items: flex-end; }
#llm-dash .fgroup { display: flex; flex-direction: column; gap: .25rem; }
#llm-dash .fgroup > label { font-size: .72rem; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); font-weight: 600; }
#llm-dash .fgroup input[type=text] { padding: .32rem .5rem; border: 1px solid var(--border); border-radius: 6px; font-size: .85rem; width: 190px; }
#llm-dash .fgroup select { padding: .32rem .4rem; border: 1px solid var(--border); border-radius: 6px; font-size: .85rem; background: #fff; }
#llm-dash .chips { display: flex; flex-wrap: wrap; gap: .3rem; max-width: 640px; }
#llm-dash .chip { font-size: .78rem; padding: .22rem .55rem; border: 1px solid var(--border); border-radius: 999px; background: #fff; cursor: pointer; user-select: none; color: var(--text); }
#llm-dash .chip.on { background: var(--accent-bg); border-color: var(--accent); color: var(--accent); font-weight: 600; }
#llm-dash .btn { font-size: .8rem; padding: .32rem .7rem; border: 1px solid var(--border); border-radius: 6px; background: #fff; cursor: pointer; }
#llm-dash .btn:hover { border-color: var(--accent); color: var(--accent); }
#llm-dash .btn.reset { color: var(--muted); }
#llm-dash .chart-card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: .9rem; margin-bottom: 1.25rem; }
#llm-dash .chart-wrap { position: relative; height: 560px; }
#llm-dash .chart-legend { font-size: .8rem; color: var(--muted); margin-top: .4rem; }
#llm-dash .countline { font-size: .85rem; color: var(--muted); margin: .4rem 0 .6rem; }
#llm-dash table.tbl { width: 100%; border-collapse: collapse; font-size: .82rem; }
#llm-dash .tbl th { text-align: left; padding: .45rem .5rem; border-bottom: 2px solid var(--border); cursor: pointer; white-space: nowrap; user-select: none; }
#llm-dash .tbl th:hover { color: var(--accent); }
#llm-dash .tbl th .arrow { font-size: .7rem; color: var(--accent); }
#llm-dash .tbl td { padding: .4rem .5rem; border-bottom: 1px solid #eaeef2; vertical-align: top; }
#llm-dash .tbl tr:hover td { background: #f0f6ff; }
#llm-dash .tbl tr.row-hl td { background: var(--accent-bg); }
#llm-dash .tbl tr.row-bic td { background: #f6fef9; box-shadow: inset 3px 0 0 var(--good); }
#llm-dash .badge { display: inline-block; font-size: .68rem; padding: .08rem .4rem; border-radius: 999px; border: 1px solid var(--border); color: var(--muted); white-space: nowrap; }
#llm-dash .badge.adaptive { color: var(--good); border-color: #7ee2a8; background: var(--good-bg); }
#llm-dash .badge.reasoning { color: var(--accent); border-color: #9cc7ff; background: var(--accent-bg); }
#llm-dash .badge.standard { color: var(--warn); border-color: #ecd9a3; background: var(--warn-bg); }
#llm-dash .num { text-align: right; font-variant-numeric: tabular-nums; }
#llm-dash .na { color: #afb8c1; }
#llm-dash .badge.open { color: var(--good); border-color: #7ee2a8; background: var(--good-bg); }
#llm-dash .badge.prop { color: #57606a; border-color: #d0d7de; background: #fff; }
#llm-dash .bic { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: .9rem 1rem; margin-top: 1rem; margin-bottom: 1.25rem; }
#llm-dash .bic h2 { font-size: 1.05rem; margin: 0 0 .15rem; }
#llm-dash .bic-sub { font-size: .8rem; color: var(--muted); margin: 0 0 .6rem; }
#llm-dash .bic-head { font-size: .74rem; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); font-weight: 600; margin: .6rem 0 .3rem; }
#llm-dash #bicList ol { margin: 0; padding-left: 1.4rem; font-size: .86rem; }
#llm-dash #bicList li { margin: .28rem 0; }
#llm-dash .bic-dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: var(--good); margin-right: .3rem; }
#llm-dash .bic-eff { color: var(--muted); font-size: .78rem; }
#llm-dash .bic-meta { color: var(--muted); }
#llm-dash .foot { font-size: .78rem; color: var(--muted); margin-top: 1.5rem; border-top: 1px solid var(--border); padding-top: .8rem; }
#llm-dash .foot a { color: var(--accent); }
@media (max-width: 800px) {
  #llm-dash .chart-wrap { height: 380px; }
  #llm-dash .tbl-wrap { overflow-x: auto; }
}
</style>

<div class="dash-header">
  <h1>LLM Intelligence vs Cost</h1>
  <p class="dash-sub">Top 50 models by Artificial Analysis Intelligence Index (v4.1), plotted against the cost to complete one intelligence-index task. Data pulled __PULLED__ from <a href="https://artificialanalysis.ai" target="_blank" rel="noopener">artificialanalysis.ai</a>. This is a snapshot, not a live benchmark.</p>
</div>

<div class="kpis" id="kpis"></div>

<div class="filters">
  <div class="fgroup">
    <label>Search</label>
    <input type="text" id="fSearch" placeholder="model name or lab..." autocomplete="off">
  </div>
  <div class="fgroup">
    <label>Creator</label>
    <div class="chips" id="fCreators"></div>
  </div>
  <div class="fgroup">
    <label>Model family</label>
    <select id="fFamily"></select>
  </div>
  <div class="fgroup">
    <label>Reasoning mode</label>
    <select id="fReasoning"></select>
  </div>
  <div class="fgroup">
    <label>License</label>
    <select id="fLicense">
      <option value="all">All</option>
      <option value="Proprietary">Proprietary</option>
      <option value="Open source">Open source</option>
    </select>
  </div>
  <div class="fgroup">
    <label>Effort level</label>
    <select id="fEffort"></select>
  </div>
  <div class="fgroup">
    <label>Min Intelligence Index</label>
    <input type="range" id="fMinII" min="0" max="65" step="1" value="0" style="width:160px">
    <span id="minIILabel" style="font-size:.78rem;color:var(--muted)">0</span>
  </div>
  <button class="btn reset" id="fReset">Reset filters</button>
</div>

<div class="chart-card">
  <div class="chart-wrap"><canvas id="scatter"></canvas></div>
  <p class="chart-legend">X axis is log-scaled cost per task (USD). Hover a point for details; click to highlight the row in the table. Models without published cost-per-task data are listed in the table but not plotted. The green step line is the <strong>best-in-class frontier</strong>: at each price it marks the highest intelligence any model achieves, so every model below the line is beaten on intelligence by a cheaper or equal-cost one.</p>
</div>

<div class="bic">
  <h2><span class="bic-dot"></span>Best in class for its price</h2>
  <p class="bic-sub">A model makes this list when no cheaper model scores higher (ties: the cheaper one wins). These are the only models that are ever the smartest choice at some budget.</p>
  <div id="bicList"></div>
</div>

<p class="countline" id="countline"></p>
<div class="tbl-wrap">
<table class="tbl" id="tbl">
  <thead><tr id="thead"></tr></thead>
  <tbody id="tbody"></tbody>
</table>
</div>

<div class="foot">
  <p><strong>Methodology.</strong> Intelligence Index v4.1 and cost-per-task figures are published by <a href="https://artificialanalysis.ai" target="_blank" rel="noopener">Artificial Analysis</a> and reproduced here with attribution. Cost per task is the USD price to complete their standard intelligence-index task set at a 3:1 input-output ratio. Where Artificial Analysis has not published a cost (4 of the top 50), the model appears in the table only. Scores from different index versions are not comparable; this snapshot uses one version throughout.</p>
  <p><strong>Best in class.</strong> The green step line connects models where no cheaper model scores higher, so it hugs the top-left edge of the point cloud; anything below the line is dominated on intelligence per dollar at its own price point. License labels reflect weights availability at the data-pull date (open-weights releases after that date are not reflected); Kimi K3 ships under its own license with commercial conditions and is counted as open source.</p>
</div>

<script>
__CHARTJS__
</script>
<script>
(function(){
const DATA = __DATA__;
const CREATOR_COLORS = {
  "OpenAI": "#0969da", "Anthropic": "#cf222e", "Google": "#1a7f37", "Alibaba": "#9a6700",
  "DeepSeek": "#8250df", "Meta": "#57606a", "Kimi": "#d1242f", "Z AI": "#1f883d",
  "SpaceXAI": "#e16f24", "MiniMax": "#0969da", "Motif Technologies": "#6e7781"
};
const REASONING_ORDER = ["Adaptive", "Reasoning", "Standard", "Non-reasoning"];
const EFFORT_ORDER = ["max", "xhigh", "high", "medium", "low", "minimal"];

let shown = DATA.slice();
let activeCreators = new Set([...new Set(DATA.map(d => d.creator))]);
let sortCol = "rank", sortAsc = true;
let chart = null;

const $ = id => document.getElementById(id);

function filter() {
  const q = $("fSearch").value.toLowerCase();
  const family = $("fFamily").value;
  const reasoning = $("fReasoning").value;
  const effort = $("fEffort").value;
  const license = $("fLicense") ? $("fLicense").value : "all";
  const minII = parseInt($("fMinII").value, 10);
  shown = DATA.filter(d => {
    if (!activeCreators.has(d.creator)) return false;
    if (family !== "all" && d.family !== family) return false;
    if (reasoning !== "all" && d.reasoning !== reasoning) return false;
    if (license !== "all" && d.license !== license) return false;
    if (effort !== "all" && d.effort !== effort) return false;
    if (d.ii < minII) return false;
    if (q && !(d.name.toLowerCase().includes(q) || d.creator.toLowerCase().includes(q))) return false;
    return true;
  });
}

// Best-in-class frontier: models where no cheaper model scores higher
// (equal-II ties go to the cheaper model). Computed on the filtered set so it
// follows the chart; only plotted models (with a published cost) can qualify.
function bicOf(list) {
  const pts = list.filter(d => d.cost != null).sort((a, b) => a.cost - b.cost || b.ii - a.ii);
  let best = -Infinity;
  const out = [];
  pts.forEach(d => {
    if (d.ii > best) { out.push(d); best = d.ii; }
  });
  const ids = new Set(out.map(d => d.rank));
  return { list: out, ids };
}

function fmtUSD(v, digits) {
  if (v == null) return '<span class="na">n/a</span>';
  const d = digits == null ? (v >= 1 ? 2 : (v >= 0.01 ? 3 : 4)) : digits;
  return "$" + v.toFixed(d);
}
function fmtNum(v, d) {
  if (v == null) return '<span class="na">n/a</span>';
  return v.toFixed(d == null ? 1 : d);
}

function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }

function renderBic(bic) {
  const el = $("bicList");
  if (!el) return;
  if (!bic.list.length) {
    el.innerHTML = '<p class="bic-sub">No plotted models match the current filters.</p>';
    return;
  }
  const cheapest = bic.list[0].cost;
  let html = '<ol>' + bic.list.map(d => {
    const meta = d.cost === cheapest ? "cheapest overall" : ("from $" + fmtUSD(d.cost).slice(1) + " per task");
    return "<li><strong>" + esc(d.name.replace(/(<|>)/g, m => m === "<" ? "&lt;" : "&gt;")) + "</strong> " +
      '<span class="badge ' + (d.license === "Open source" ? "open" : "prop") + '">' + d.license + '</span> ' +
      '<span class="bic-meta">· ' + d.creator + ' · II ' + d.ii + ' · ' + meta + '</span></li>';
  }).join("") + "</ol>";
  html += '<p class="bic-eff">' + bic.list.length + ' of ' +
    shown.filter(d => d.cost != null).length + ' plotted models sit on the frontier under the current filters.</p>';
  el.innerHTML = html;
}

function kpis(bic) {
  const withCost = shown.filter(d => d.cost != null);
  const best = [...withCost].sort((a, b) => (b.ii / b.cost) - (a.ii / a.cost))[0];
  const top = shown.length ? shown.reduce((a, b) => a.ii > b.ii ? a : b) : null;
  const cheapest = withCost.length ? withCost.reduce((a, b) => a.cost < b.cost ? a : b) : null;
  const medianCost = withCost.length ? withCost.map(d => d.cost).sort((a, b) => a - b)[Math.floor(withCost.length / 2)] : null;
  const cards = [
    ["Models shown", String(shown.length), "of " + DATA.length + " in the ranking"],
    ["Top intelligence", top ? (top.name.split(" (")[0].slice(0, 28) + " · " + top.ii) : "n/a", ""],
    ["Best value", best ? (best.name.split(" (")[0].slice(0, 24) + " · " + (best.ii / best.cost).toFixed(0) + " II/$") : "n/a", "intelligence per dollar"],
    ["Median cost/task", medianCost != null ? fmtUSD(medianCost) : "n/a", "of models with published cost"],
    ["Best-in-class models", String(bic.list.length), "on the price frontier"],
  ];
  $("kpis").innerHTML = cards.map(c =>
    '<div class="kpi"><div class="k-label">' + c[0] + '</div><div class="k-value" title="' + esc(c[1]) + '">' + c[1] + '</div><div class="k-note">' + c[2] + '</div></div>'
  ).join("");
}

function renderChart(bic) {
  const plotted = shown.filter(d => d.cost != null);
  const datasets = [];
  const creators = [...new Set(plotted.map(d => d.creator))].sort();
  creators.forEach(cr => {
    const pts = plotted.filter(d => d.creator === cr).map(d => ({
      x: d.cost, y: d.ii, name: d.name, creator: d.creator, coding: d.coding,
      tok_s: d.tok_s, price_in: d.price_in, price_out: d.price_out, rank: d.rank
    }));
    datasets.push({
      label: cr, data: pts, backgroundColor: CREATOR_COLORS[cr] || "#6e7781",
      pointRadius: 5, pointHoverRadius: 7, borderWidth: 0,
    });
  });
  // best-in-class frontier as a green step line through the top-left corner
  if (bic.list.length) {
    datasets.push({
      type: "line",
      label: "Best in class (price frontier)",
      data: bic.list.map(d => ({ x: d.cost, y: d.ii })),
      borderColor: "#1a7f37", backgroundColor: "transparent",
      borderWidth: 2, pointRadius: 0, pointHitRadius: 0,
      fill: false, tension: 0, stepped: "after",
      order: -1,
    });
  }
  const ctx = $("scatter").getContext("2d");
  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: "scatter",
    data: { datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: "nearest", intersect: true },
      onClick: (evt, el) => {
        if (!el.length) return;
        const idx = el[0].datasetIndex, pidx = el[0].index;
        const d = chart.data.datasets[idx].data[pidx];
        const row = document.querySelector('tr[data-rank="' + d.rank + '"]');
        if (row) {
          row.scrollIntoView({ behavior: "smooth", block: "center" });
          row.classList.add("row-hl");
          setTimeout(() => row.classList.remove("row-hl"), 2500);
        }
      },
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 10, boxHeight: 10, padding: 14, font: { size: 11 } } },
        tooltip: {
          callbacks: {
            label: (c) => {
              const d = c.raw;
              if (!d.name) return ""; // frontier line points carry no model info
              return [
                d.name,
                "Intelligence: " + d.y,
                "Cost/task: $" + d.x.toFixed(4),
                "Coding index: " + (d.coding != null ? d.coding : "n/a"),
                "Output: " + (d.tok_s != null ? d.tok_s.toFixed(0) + " tok/s" : "n/a"),
                "Price: $" + (d.price_in != null ? d.price_in : "?") + " in / $" + (d.price_out != null ? d.price_out : "?") + " out (per 1M)"
              ];
            }
          }
        }
      },
      scales: {
        x: { type: "logarithmic", title: { display: true, text: "Cost per task (USD, log scale)" }, grid: { color: "#eaeef2" } },
        y: { title: { display: true, text: "Intelligence Index (v4.1)" }, grid: { color: "#eaeef2" } }
      }
    }
  });
}

function renderTable(bic) {
  const cols = [
    { k: "rank", label: "#", cls: "num" },
    { k: "name", label: "Model" },
    { k: "creator", label: "Lab" },
    { k: "family", label: "Family" },
    { k: "license", label: "License" },
    { k: "reasoning", label: "Reasoning" },
    { k: "effort", label: "Effort" },
    { k: "ii", label: "Intelligence", cls: "num" },
    { k: "coding", label: "Coding", cls: "num" },
    { k: "cost", label: "Cost/task", cls: "num" },
    { k: "price_in", label: "$ in", cls: "num" },
    { k: "price_out", label: "$ out", cls: "num" },
    { k: "tok_s", label: "tok/s", cls: "num" },
    { k: "release", label: "Released" },
  ];
  const rows = shown.slice().sort((a, b) => {
    let va = a[sortCol], vb = b[sortCol];
    if (va == null) return 1; if (vb == null) return -1;
    return sortAsc ? (va > vb ? 1 : -1) : (va < vb ? 1 : -1);
  });
  $("thead").innerHTML = "<th></th>" + cols.map(c =>
    '<th data-k="' + c.k + '" class="' + (c.cls || "") + '">' + c.label +
    (sortCol === c.k ? ' <span class="arrow">' + (sortAsc ? "▲" : "▼") + "</span>" : "") + "</th>"
  ).join("");
  $("thead").querySelectorAll("th[data-k]").forEach(th => th.onclick = () => {
    const k = th.dataset.k;
    if (sortCol === k) sortAsc = !sortAsc; else { sortCol = k; sortAsc = k === "rank"; }
    renderTable();
  });
  $("tbody").innerHTML = rows.map(d => {
    const badges = [];
    if (d.reasoning === "Adaptive") badges.push('<span class="badge adaptive">Adaptive</span>');
    else if (d.reasoning === "Reasoning") badges.push('<span class="badge reasoning">Reasoning</span>');
    else if (d.reasoning === "Standard") badges.push('<span class="badge standard">Standard</span>');
    const onFrontier = bic.ids.has(d.rank);
    const star = onFrontier ? '<span class="bic-dot" title="Best in class for its price"></span>' : "";
    return "<tr data-rank=\"" + d.rank + "\"" + (onFrontier ? ' class="row-bic"' : "") + ">" +
      "<td class=\"num\">" + d.rank + "</td>" +
      "<td>" + star + "<strong>" + d.name.replace(/(<|>)/g, m => m === "<" ? "&lt;" : "&gt;") + "</strong></td>" +
      "<td>" + d.creator + "</td>" +
      "<td>" + d.family + "</td>" +
      "<td>" + (d.license ? '<span class="badge ' + (d.license === "Open source" ? "open" : "prop") + '">' + d.license + '</span>' : "") + "</td>" +
      "<td>" + badges.join("") + "</td>" +
      "<td>" + (d.effort ? d.effort : '<span class="na">-</span>') + "</td>" +
      "<td class=\"num\">" + fmtNum(d.ii) + "</td>" +
      "<td class=\"num\">" + fmtNum(d.coding) + "</td>" +
      "<td class=\"num\">" + fmtUSD(d.cost) + "</td>" +
      "<td class=\"num\">" + (d.price_in != null ? "$" + d.price_in.toFixed(2) : '<span class="na">n/a</span>') + "</td>" +
      "<td class=\"num\">" + (d.price_out != null ? "$" + d.price_out.toFixed(2) : '<span class="na">n/a</span>') + "</td>" +
      "<td class=\"num\">" + fmtNum(d.tok_s, 0) + "</td>" +
      "<td>" + (d.release || '-') + "</td>" +
      "</tr>";
  }).join("");
  $("countline").textContent = shown.length + " of " + DATA.length + " models shown" +
    (shown.length < DATA.length ? " (filters active)" : "");
}

function render() {
  filter();
  const bic = bicOf(shown);
  kpis(bic);
  renderChart(bic);
  renderTable(bic);
  renderBic(bic);
}

function initControls() {
  const creators = [...new Set(DATA.map(d => d.creator))].sort();
  $("fCreators").innerHTML = creators.map(c =>
    '<span class="chip on" data-cr="' + c + '">' + c + '</span>'
  ).join("");
  $("fCreators").querySelectorAll(".chip").forEach(ch => ch.onclick = () => {
    const cr = ch.dataset.cr;
    if (activeCreators.has(cr)) { activeCreators.delete(cr); ch.classList.remove("on"); }
    else { activeCreators.add(cr); ch.classList.add("on"); }
    render();
  });
  const FAMILY_ORDER = ["Claude", "GPT", "Gemini", "Qwen", "Grok", "DeepSeek", "Kimi", "GLM", "Muse", "MiniMax", "Motif"];
  $("fFamily").innerHTML = '<option value="all">All families</option>' +
    FAMILY_ORDER.filter(f => DATA.some(d => d.family === f)).map(f => '<option value="' + f + '">' + f + '</option>').join("");
  $("fReasoning").innerHTML = '<option value="all">All modes</option>' +
    REASONING_ORDER.map(r => '<option value="' + r + '">' + r + '</option>').join("");
  $("fEffort").innerHTML = '<option value="all">Any effort</option>' +
    EFFORT_ORDER.map(e => '<option value="' + e + '">' + e + '</option>').join("");
  ["fFamily", "fReasoning", "fEffort", "fLicense"].forEach(id => $(id).onchange = render);
  $("fSearch").oninput = render;
  $("fMinII").oninput = () => { $("minIILabel").textContent = $("fMinII").value; render(); };
  $("fReset").onclick = () => {
    activeCreators = new Set([...new Set(DATA.map(d => d.creator))]);
    $("fCreators").querySelectorAll(".chip").forEach(ch => ch.classList.add("on"));
    $("fSearch").value = ""; $("fFamily").value = "all"; $("fReasoning").value = "all"; $("fEffort").value = "all";
    if ($("fLicense")) $("fLicense").value = "all";
    $("fMinII").value = 0; $("minIILabel").textContent = "0";
    render();
  };
}

initControls();
render();
})();
</script>
</div>
'''

if __name__ == "__main__":
    main()