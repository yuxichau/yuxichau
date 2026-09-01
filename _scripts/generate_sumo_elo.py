#!/usr/bin/env python3
"""Generate _pages/sumo-elo.html -- All-Division Sumo Elo Explorer.

Source dataset: window.SUMO_DATA = {bashos:[...], rikishi:[[id,name,debutIdx,peak,peakIdx]...],
series:{id:[bashoIdx,rating,divCode,...]}} -- produced by /root/sumo-elo/gen_dashboard_data.py
(sumo-api.com banzuke data, day-by-day Elo replay 1958-2026, K=64, fusen/kyujo excluded,
no decay, all six divisions).

Regenerate after the VM pipeline updates the dataset:
    cp /root/sumo-elo/outputs/sumo-data.js _scripts/data/sumo_elo_data.js
    python3 _scripts/generate_sumo_elo.py
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_scripts", "data", "sumo_elo_data.js")
CHART = os.path.join(ROOT, "_scripts", "vendor", "chart.umd.js")
PAGE = os.path.join(ROOT, "_pages", "sumo-elo.html")
ASSET = os.path.join(ROOT, "assets", "js", "sumo-elo-data.js")

# ---- read vendored pieces ----
with open(DATA, encoding="utf-8") as fh:
    data_js = fh.read()
with open(CHART, encoding="utf-8") as fh:
    chart_js = fh.read()
# strip sourceMappingURL trailer (map isn't served; avoids console 404)
chart_js = re.sub(r"//# sourceMappingURL=.*$", "", chart_js, flags=re.M)

FRONT = """---
layout: single
title: "All-Division Sumo Elo Explorer"
classes: wide
author_profile: false
permalink: /projects/sumo-elo/
---"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>All-Division Sumo Elo Explorer</title>
</head>
<body>
<div id="sep-app">
<style>
#sep-app { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif; color:#1f2328; line-height:1.5; }
#sep-app .sub { color:#57606a; margin:0 0 .9rem; font-size:.95rem; }
#sep-app h1.sep { margin-top:0; font-size:1.5rem; letter-spacing:-.3px; }
#sep-app .kpis { display:grid; grid-template-columns:repeat(auto-fit,minmax(155px,1fr)); gap:.7rem; margin-bottom:1.1rem; }
#sep-app .kpi { background:#f6f8fa; border:1px solid #d0d7de; border-radius:8px; padding:.65rem .9rem; }
#sep-app .kpi .k-label { font-size:.72rem; text-transform:uppercase; letter-spacing:.04em; color:#57606a; }
#sep-app .kpi .k-value { font-size:1.1rem; font-weight:600; margin-top:.15rem; }
#sep-app .kpi .k-value small { font-weight:400; color:#57606a; font-size:.78rem; }
#sep-app .panel { background:#f6f8fa; border:1px solid #d0d7de; border-radius:8px; padding:.9rem 1rem; margin-bottom:1.1rem; }
#sep-app h2 { font-size:1.05rem; margin:0 0 .6rem; border-bottom:none; padding-bottom:0; }
#sep-app .controls { display:flex; flex-wrap:wrap; gap:.5rem; align-items:center; margin-bottom:.7rem; }
#sep-app .ctl-label { font-size:.8rem; color:#57606a; font-weight:600; }
#sep-app button.pill { font-size:.8rem; padding:.3rem .8rem; border:1px solid #d0d7de; background:#fff; color:#57606a; border-radius:100px; cursor:pointer; }
#sep-app button.pill.active { background:#0969da; border-color:#0969da; color:#fff; }
#sep-app select.sel { font-size:.85rem; padding:.25rem .4rem; border:1px solid #d0d7de; border-radius:6px; background:#fff; color:#1f2328; max-width:9.5rem; }
#sep-app input[type=text] { font-size:.85rem; padding:.35rem .5rem; border:1px solid #d0d7de; border-radius:6px; width:250px; max-width:100%; }
#sep-app .searchbox { position:relative; }
#sep-app .search-results { position:absolute; top:32px; left:0; width:320px; background:#fff; border:1px solid #d0d7de; border-radius:6px; box-shadow:0 8px 24px rgba(0,0,0,.12); z-index:20; max-height:300px; overflow:auto; display:none; }
#sep-app .search-results div { padding:6px 11px; font-size:.85rem; cursor:pointer; }
#sep-app .search-results div:hover { background:#ddf4ff; }
#sep-app .chart-lines { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:.6rem; }
#sep-app .chart-lines .label { color:#57606a; font-size:.78rem; text-transform:uppercase; letter-spacing:.04em; }
#sep-app .chips { display:flex; flex-wrap:wrap; gap:6px; }
#sep-app .chip { display:inline-flex; align-items:center; gap:5px; background:#ddf4ff; color:#0969da; border:1px solid rgba(9,105,218,.35); border-radius:100px; padding:2px 6px 2px 11px; font-size:.82rem; }
#sep-app .chip button { border:none; background:none; color:#57606a; cursor:pointer; font-size:1rem; line-height:1; padding:0 4px; }
#sep-app .chart-wrap { position:relative; height:400px; background:#fff; border:1px solid #d0d7de; border-radius:8px; padding:.5rem; }
#sep-app .chart-note { font-size:.8rem; color:#656d76; margin-top:.5rem; }
#sep-app .view-tabs { display:flex; gap:.4rem; margin-bottom:.7rem; }
#sep-app .view-tab { font-size:.82rem; padding:.35rem .8rem; border:1px solid #d0d7de; background:#fff; color:#57606a; border-radius:6px; cursor:pointer; }
#sep-app .view-tab.active { background:#0969da; border-color:#0969da; color:#fff; }
#sep-app .div-filter { display:flex; flex-wrap:wrap; gap:.5rem .8rem; align-items:center; margin-bottom:.6rem; font-size:.85rem; }
#sep-app .div-filter label { color:#57606a; display:inline-flex; align-items:center; gap:4px; cursor:pointer; }
#sep-app .tbl-wrap { max-height:460px; overflow:auto; border:1px solid #d0d7de; border-radius:6px; background:#fff; }
#sep-app table { width:100%; border-collapse:collapse; font-size:.88rem; }
#sep-app th, #sep-app td { border-bottom:1px solid #d8dee4; padding:5px 10px; text-align:left; }
#sep-app th { background:#f6f8fa; font-weight:600; position:sticky; top:0; }
#sep-app td.num { text-align:right; font-variant-numeric:tabular-nums; }
#sep-app tr:hover td { background:#f6f8fa; }
#sep-app .up { color:#1a7f37; } #sep-app .down { color:#cf222e; }
#sep-app .muted { color:#57606a; font-size:.88rem; }
#sep-app ul.clean { padding-left:18px; margin:8px 0; color:#57606a; font-size:.9rem; line-height:1.65; }
#sep-app ul.clean li { margin-bottom:5px; }
#sep-app a { color:#0969da; }
@media(max-width:700px){ #sep-app .chart-wrap{height:320px;} #sep-app .search-results{width:260px;} }
</style>

<h1 class="sep">All-Division Sumo Elo Explorer</h1>
<p class="sub">Every honbasho bout replayed day-by-day, Mar 1958 to Jul 2026 &bull; K=64 &bull; all six divisions &bull; ky&#363;j&#333;/fusen excluded &bull; no decay</p>

<div class="kpis" id="sep-kpis"></div>

<div class="panel">
  <h2>Rikishi explorer</h2>
  <div class="view-tabs" role="tablist" aria-label="Rating view">
    <button class="view-tab active" data-view="raw" role="tab" aria-selected="true">Raw Elo</button>
    <button class="view-tab" data-view="calibrated" role="tab" aria-selected="false">Calibrated Elo</button>
  </div>
  <div class="controls">
    <div class="searchbox">
      <input type="text" id="sep-q" placeholder="Search rikishi (e.g. Hakuho, Terunofuji, Aonishiki...)" autocomplete="off">
      <div class="search-results" id="sep-qr"></div>
    </div>
  </div>
  <div class="chart-wrap"><canvas id="sep-chart"></canvas></div>
  <div class="chart-lines"><span class="label">Chart lines</span><span class="chips" id="sep-chips"></span></div>
  <div class="chart-note" id="sep-note"></div>
</div>

<div class="panel">
  <h2>Top 50 by peak calibrated Elo</h2>
  <p class="muted">The baseline is recalculated after every basho, using that basho's top-50 mean. The latest completed basho provides the reference scale. The date is when the calibrated peak was obtained.</p>
  <div class="tbl-wrap"><table><thead><tr><th>#</th><th>Rikishi</th><th class="num">Peak calibrated Elo</th><th>Date obtained</th><th class="num">Raw Elo then</th></tr></thead><tbody id="sep-cal-lb"></tbody></table></div>
</div>

<div class="panel">
  <h2>Leaderboard &mdash; rating at end of window</h2>
  <div class="controls">
    <span class="ctl-label">From</span> <select class="sel" id="sep-from"></select>
    <span class="ctl-label">To</span> <select class="sel" id="sep-to"></select>
    <button class="pill preset active" data-preset="all">All</button>
    <button class="pill preset" data-preset="10">10Y</button>
    <button class="pill preset" data-preset="20">20Y</button>
    <button class="pill preset" data-preset="30">30Y</button>
  </div>
  <div class="div-filter" id="sep-divfilter"></div>
  <div class="tbl-wrap">
    <table>
      <thead><tr><th>#</th><th>Rikishi</th><th>Division @end</th><th class="num">Elo</th><th class="num">&Delta; since start</th><th>Peak</th></tr></thead>
      <tbody id="sep-lb"></tbody>
    </table>
  </div>
</div>

<div class="panel">
  <h2>Methodology</h2>
  <ul class="clean">
    <li><strong>Seeding.</strong> Every rikishi starts at the baseline of the division they first appeared in (Yokozuna 2800, &#332;zeki 2600, Sekiwake 2480, Komusubi 2420, Maegashira 2275, J&#363;ry&#333; 2100, Makushita 1900, Sandanme 1700, Jonidan 1550, Jonokuchi 1500). New entrants (including makushita tsukedashi) are seeded by their debut rank automatically.</li>
    <li><strong>Update.</strong> Elo with K=64 and scale 400, applied bout-by-bout in chronological order across all six divisions. A high K keeps ratings responsive to current form, which suits short sumo careers.</li>
    <li><strong>ky&#363;j&#333;.</strong> Withdrawals and forfeit (fusen) bouts are not wins or losses: neither side's rating moves. Only contested bouts count.</li>
    <li><strong>No decay.</strong> An absent rikishi's rating is frozen, so the rating pool is conserved across 68 years.</li>
    <li><strong>Coverage.</strong> Makuuchi and J&#363;ry&#333; have full bout records from Mar 1958. The four lower divisions have full bout records from Jan 1988; before that only aggregate W/L was published, so those rikishi hold their seed rating until 1988 or until they reach a sekitori division.</li>
    <li><strong>Calibration.</strong> After each basho, the mean Elo of the top 50 rated rikishi is calculated. A rating is adjusted as raw Elo minus that basho's top-50 mean, plus the top-50 mean at the latest completed basho. This is a basho-level location adjustment, not an annual average.</li>
    <li><strong>Cross-era caution.</strong> Raw Elo is a within-pool performance measure, not an era-adjusted GOAT score. Later careers face a larger, deeper recorded pool and can accumulate higher ratings; compare a rikishi with the leaders of his own era as well as by raw peak.</li>
    <li><strong>Shikona.</strong> Names are the rikishi's latest ring name (Terunofuji debuted as Wakamisho; Kotozakura as Kotokamatani; Chiyonofuji as Oakimoto).</li>
    <li><strong>Data.</strong> 748,204 bouts reconstructed from sumo-api.com banzuke records (both rikishi's entries cross-checked; 3,517 fusen excluded). 9,048 rikishi rated across 409 bashos.</li>
  </ul>
</div>

<script>
/* vendored Chart.js 4.x */
__CHART_JS__
</script>
<script src="/assets/js/sumo-elo-data.js"></script>
<script>
(function(){
const D = window.SUMO_DATA;
const bashos = D.bashos, rikishi = D.rikishi, series = D.series;
const DIVS = ["Makuuchi","Jūryō","Makushita","Sandanme","Jonidan","Jonokuchi"];
const PALETTE = ["#0969da","#cf222e","#1a7f37","#9a6700","#8250df","#0550ae","#d1242f","#116329","#bc4c00","#563d7c","#0a3069","#953800"];
let fromIdx = 0, toIdx = bashos.length - 1;
let selected = [], activeDims = [true,true,true,true,true,true];
let view = "raw";

// Additive location adjustment using the top-50 mean at each basho.
const ratingsByBasho = bashos.map(()=>[]);
for (const id in series) { const s=series[id]; for(let i=0;i+2<s.length;i+=3) ratingsByBasho[s[i]].push(s[i+1]); }
const top50Mean = ratingsByBasho.map(xs=>{ const a=xs.slice().sort((a,b)=>b-a).slice(0,50); return a.length ? a.reduce((x,y)=>x+y,0)/a.length : null; });
const referenceBaseline = top50Mean[top50Mean.length-1];
function calibratedValue(raw, idx){ return raw - top50Mean[idx] + referenceBaseline; }

const $ = id => document.getElementById(id);

function kpi(label, value){ const d = document.createElement("div"); d.className="kpi";
  d.innerHTML = `<div class="k-label">${label}</div><div class="k-value">${value}</div>`; $("sep-kpis").appendChild(d); }

const fromSel = $("sep-from"), toSel = $("sep-to");
bashos.forEach((b,i)=>{ fromSel.add(new Option(b,i)); toSel.add(new Option(b,i)); });
fromSel.value = "0"; toSel.value = String(bashos.length-1);

const dfl = $("sep-divfilter");
DIVS.forEach((d,i)=>{ const l = document.createElement("label");
  l.innerHTML = `<input type="checkbox" data-d="${i}" checked> ${d}`; dfl.appendChild(l); });
dfl.addEventListener("change", e=>{ if(e.target.dataset.d !== undefined){ activeDims[+e.target.dataset.d]=e.target.checked; renderLb(); }});

const q = $("sep-q"), qr = $("sep-qr");
const norm = s => s.toLowerCase().replace(/[^a-z0-9]/g,"");
q.addEventListener("input", ()=>{
  const t = norm(q.value);
  if (t.length < 2){ qr.style.display="none"; return; }
  const hits = [];
  for (const r of rikishi){ if (norm(r[1]).includes(t)){ hits.push(r); if (hits.length>=12) break; } }
  qr.innerHTML = "";
  if (!hits.length){ qr.style.display="none"; return; }
  hits.forEach(r=>{ const d=document.createElement("div");
    d.textContent = `${r[1]} — debut ${bashos[r[2]]} · peak ${r[3]} · ID ${r[0]}`;
    d.onclick = ()=>{ addRikishi(r[0]); q.value=""; qr.style.display="none"; }; qr.appendChild(d); });
  qr.style.display="block";
});
document.addEventListener("click", e=>{ if(!e.target.closest(".searchbox")) qr.style.display="none"; });

function ro(id){ for (const r of rikishi) if (r[0]===id) return r; return null; }
function addRikishi(id){
  if (selected.includes(id)) return;
  selected.push(id);
  if (selected.length > 8) selected.shift();
  renderChips(); renderChart();
}
function removeRikishi(id){ selected = selected.filter(x=>x!==id); renderChips(); renderChart(); }
function renderChips(){
  const c = $("sep-chips"); c.innerHTML = "";
  selected.forEach(id=>{ const r = ro(id);
    const sp = document.createElement("span"); sp.className="chip";
    sp.innerHTML = `${r[1]} <button onclick="removeRikishi(${id})">&times;</button>`; c.appendChild(sp); });
}

const mainChart = new Chart($("sep-chart"), {
  type:"line", data:{ labels: [], datasets: [] },
  options:{ responsive:true, maintainAspectRatio:false,
    interaction:{ mode:"nearest", intersect:false },
    plugins:{ legend:{ display:false, position:"top", labels:{ boxWidth:12, font:{size:11} } },
      tooltip:{ callbacks:{ title: items=>bashos[items[0].dataIndex] } } },
    scales:{ x:{ grid:{display:false}, ticks:{ maxTicksLimit:12, font:{size:10} } },
      y:{ grid:{color:"#eef1f4"}, ticks:{ font:{size:10} }, title:{display:true,text:"Elo",color:"#57606a"} } } }
});
window.mainChart = mainChart;

function renderChart(){
  // Compress the chart to the union of the selected rikishi's active dates.
  // The leaderboard window still controls the available outer bounds.
  let chartFrom = fromIdx, chartTo = toIdx;
  if (selected.length) {
    const available = [];
    selected.forEach(id=>{
      const s = series[id];
      if (!s) return;
      for (let i=0;i+2<s.length;i+=3) if (s[i]>=fromIdx && s[i]<=toIdx) available.push(s[i]);
    });
    if (available.length) { chartFrom=Math.min(...available); chartTo=Math.max(...available); }
  }
  const labels = bashos.slice(chartFrom, chartTo+1);
  mainChart.options.plugins.legend.display = selected.length>1 && selected.length<=8;
  mainChart.data = { labels, datasets: [] };
  selected.forEach((id,si)=>{
    const s = series[id]; if (!s) return;
    const byIdx = new Map();
    for (let i=0;i+2<s.length;i+=3){ const bi=s[i]; if (bi>=chartFrom && bi<=chartTo) byIdx.set(bi, s[i+1]); }
    const data = labels.map((_,k)=>byIdx.has(chartFrom+k) ? (view==="raw" ? byIdx.get(chartFrom+k) : calibratedValue(byIdx.get(chartFrom+k), chartFrom+k)) : null);
    mainChart.data.datasets.push({ label: (ro(id)||{1:String(id)})[1], data,
      borderColor: PALETTE[si%PALETTE.length], backgroundColor: PALETTE[si%PALETTE.length]+"22",
      fill:false, pointRadius:0, borderWidth:2, spanGaps:false, tension:.15 });
  });
  mainChart.options.scales.y.title.text = view==="raw" ? "Raw Elo" : "Calibrated Elo";
  mainChart.update();
  $("sep-note").textContent = selected.length
    ? (view==="raw" ? "Raw Elo. The x-axis spans the selected rikishi's available dates; gaps are bashos where a selected rikishi was not on a banzuke (kyujo / retirement)." : `Calibrated Elo = raw Elo − top-50 mean at that basho + ${Math.round(referenceBaseline)}. This removes movement in the elite-field baseline while preserving contemporaneous gaps.`)
    : "Search and add rikishi above to plot their Elo curves.";
}

function ratingAt(id, idx){
  const s = series[id]; if (!s) return null;
  let best = null;
  for (let i=0;i+2<s.length;i+=3){ if (s[i] > idx) break; best = [s[i+1], s[i+2], s[i]]; }
  return best;
}
function calibratedAt(id, idx){ const at=ratingAt(id,idx); return at ? [calibratedValue(at[0], at[2]),at[1],at[2]] : null; }
function renderLb(){
  const rows = [];
  for (const r of rikishi){
    const at = view==="raw" ? ratingAt(r[0], toIdx) : calibratedAt(r[0], toIdx), st = view==="raw" ? ratingAt(r[0], fromIdx) : calibratedAt(r[0], fromIdx);
    if (!at) continue;
    if (!activeDims[at[1]]) continue;
    const s = series[r[0]]; let inWin = false;
    for (let i=0;i+2<s.length;i+=3){ if (s[i]>=fromIdx && s[i]<=toIdx){ inWin=true; break; } }
    if (!inWin) continue;
    rows.push({ id:r[0], name:r[1], div:at[1], elo:at[0], delta:st ? at[0]-st[0] : null, peak:r[3] });
  }
  rows.sort((a,b)=>b.elo-a.elo);
  const tb = $("sep-lb"); tb.innerHTML = "";
  rows.slice(0,100).forEach((row,i)=>{
    const tr = document.createElement("tr");
    const dl = row.delta===null ? "&mdash;" : (row.delta>=0?`<span class="up">+${row.delta}</span>`:`<span class="down">${row.delta}</span>`);
    tr.innerHTML = `<td>${i+1}</td><td><a href="#" onclick="event.preventDefault();addRikishi(${row.id})">${row.name}</a></td>
      <td>${DIVS[row.div]}</td><td class="num">${Math.round(row.elo)}</td><td class="num">${dl}</td><td class="num">${row.peak}</td>`;
    tb.appendChild(tr);
  });
  if (!rows.length) tb.innerHTML = `<tr><td colspan="6" class="muted">No rikishi in this window/division selection.</td></tr>`;
}

function renderCalibratedLb(){
  const rows=[];
  for(const r of rikishi){ const s=series[r[0]]; if(!s) continue; let best=null;
    for(let i=0;i+2<s.length;i+=3){ const v=calibratedValue(s[i+1],s[i]); if(!best || v>best.elo) best={elo:v,idx:s[i],raw:s[i+1]}; }
    if(best) rows.push({name:r[1],id:r[0],elo:best.elo,idx:best.idx,raw:best.raw});
  }
  rows.sort((a,b)=>b.elo-a.elo); const tb=$("sep-cal-lb"); tb.innerHTML="";
  rows.slice(0,50).forEach((x,i)=>{ const tr=document.createElement("tr"); tr.innerHTML=`<td>${i+1}</td><td><a href="#" onclick="event.preventDefault();addRikishi(${x.id})">${x.name}</a></td><td class="num">${Math.round(x.elo)}</td><td>${bashos[x.idx]}</td><td class="num">${Math.round(x.raw)}</td>`; tb.appendChild(tr); });
}

document.querySelectorAll("#sep-app .view-tab").forEach(b=>b.addEventListener("click",()=>{
  view=b.dataset.view; document.querySelectorAll("#sep-app .view-tab").forEach(x=>{x.classList.toggle("active",x===b);x.setAttribute("aria-selected",x===b?"true":"false")}); renderChart(); renderLb();
}));

function setWindow(f,t){
  fromIdx=f; toIdx=t; fromSel.value=String(f); toSel.value=String(t);
  document.querySelectorAll("#sep-app .preset").forEach(b=>b.classList.toggle("active", b.dataset.preset==="all" && f===0 && t===bashos.length-1));
  renderChart(); renderLb();
}
fromSel.addEventListener("change", e=>{ fromIdx=+e.target.value; if (fromIdx>toIdx) toIdx=fromIdx, toSel.value=fromIdx; renderChart(); renderLb(); });
toSel.addEventListener("change", e=>{ toIdx=+e.target.value; if (toIdx<fromIdx) fromIdx=toIdx, fromSel.value=toIdx; renderChart(); renderLb(); });
document.querySelectorAll("#sep-app .preset").forEach(b=>{
  b.addEventListener("click", ()=>{
    const n = bashos.length;
    if (b.dataset.preset==="all") setWindow(0, n-1);
    else setWindow(Math.max(0, n-1-(+b.dataset.preset)*6), n-1);
  });
});

(function init(){
  const best = rikishi.slice().sort((a,b)=>b[3]-a[3]).slice(0,1)[0];
  kpi("Bashos", bashos.length);
  kpi("Rikishi rated", rikishi.length.toLocaleString());
  kpi("Bouts replayed", "748,204");
  kpi("All-time #1", `${best[1]} <small>${best[3]}</small>`);
  // Stable IDs avoid selecting the older Hakuho (ID 2090) by name.
  [3081,45,8854,20].forEach(id=>{ if (ro(id)) addRikishi(id); });
  renderLb();
  renderCalibratedLb();
})();
})();
</script>
</div>
</body>
</html>
"""

# ---- emit page + static asset ----
os.makedirs(os.path.dirname(ASSET), exist_ok=True)
os.makedirs(os.path.dirname(PAGE), exist_ok=True)
with open(PAGE, "w", encoding="utf-8") as fh:
    fh.write(FRONT.rstrip() + "\n\n" + PAGE_TEMPLATE.replace("__CHART_JS__", chart_js))
with open(ASSET, "w", encoding="utf-8") as fh:
    fh.write(data_js)
print(f"wrote {PAGE} ({os.path.getsize(PAGE)/1024:.0f} KB) and {ASSET} "
      f"({os.path.getsize(ASSET)/1024/1024:.1f} MB)")