#!/usr/bin/env python3
"""Generate the self-contained OpenCode Go frontier page from vendored data."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/"_scripts/data/opencode_go_frontier.json"
PAGE=ROOT/"_pages/opencode-go-frontier-analysis.html"
CHART=ROOT/"_scripts/vendor/chart.umd.js"
TEMPLATE=r'''---
layout: single
title: "OpenCode Go Frontier Analysis"
classes: wide
author_profile: false
permalink: /projects/opencode-go-frontier-analysis/
---
<div id="go-frontier">
<style>
#go-frontier{--bg:#fff;--card:#f6f8fa;--line:#d0d7de;--ink:#1f2328;--muted:#57606a;--blue:#0969da;--bluebg:#ddf4ff;--green:#1a7f37;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);line-height:1.5}
#go-frontier h2{font-size:1.8rem;margin:0 0 .25rem}#go-frontier h3{font-size:1.05rem;margin:1.2rem 0 .35rem}.sub{color:var(--muted);margin:0 0 1rem;font-size:.95rem}.sub a,.foot a{color:var(--blue)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:.7rem;margin:1rem 0 1.2rem}.kpi,.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:.75rem .9rem}.klabel{font-size:.7rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}.kvalue{font-size:1.2rem;font-weight:650}.knote{font-size:.77rem;color:var(--muted)}
.card{margin-bottom:1.2rem}.chart{height:550px;position:relative}.legend{font-size:.8rem;color:var(--muted)}table{width:100%;border-collapse:collapse;font-size:.8rem}th,td{text-align:left;padding:.42rem .48rem;border-bottom:1px solid #eaeef2;vertical-align:top}th{border-bottom:2px solid var(--line);white-space:nowrap}.num{text-align:right;font-variant-numeric:tabular-nums}.frontier{background:#f0fdf4}.foot{border-top:1px solid var(--line);padding-top:.8rem;color:var(--muted);font-size:.78rem}.formula{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#fff;border:1px solid var(--line);padding:.5rem;overflow:auto;font-size:.78rem}@media(max-width:800px){.chart{height:390px}.table-wrap{overflow-x:auto}}
</style>
<h2>OpenCode Go Frontier Analysis</h2>
<p class="sub">Artificial Analysis Intelligence Index v__VERSION__ against the estimated share of OpenCode Go's model-specific monthly usage consumed by one benchmark task. Data pulled __DATE__. Sources: <a href="https://artificialanalysis.ai" target="_blank" rel="noopener">Artificial Analysis</a> and <a href="https://opencode.ai/v2/docs/console/go" target="_blank" rel="noopener">OpenCode Go pricing and limits</a>.</p>
<div class="kpis" id="kpis"></div>
<div class="card"><div class="chart"><canvas id="chart"></canvas></div><p class="legend">The green line is the frontier: after sorting by Go usage share, each point is retained when no cheaper model has a higher Intelligence Index. Hover points for the model, proxy cost, and quota contribution.</p></div>
<div class="card"><h3>What the percentage means</h3><p>OpenCode publishes a monthly dollar allowance for each model, rather than a request quota. This chart estimates how much of that allowance one Artificial Analysis task would consume if run through Go's published prices and observed request pattern. A lower percentage means more benchmark-equivalent tasks per month.</p><div class="formula">Go proxy = AA task cost × (Go effective $/1M tokens ÷ AA published 3:1 $/1M tokens); contribution = Go proxy ÷ Go monthly usage allowance × 100</div><p class="knote">The proxy uses OpenCode's documented typical input, cached-read, and output tokens. Cached-write is omitted because the Go usage examples do not specify writes. It is a comparison instrument, not an invoice estimate.</p></div>
<div class="card"><h3>Model detail</h3><div class="table-wrap"><table><thead><tr><th>Model</th><th>AA model used</th><th class="num">II</th><th class="num">AA task $</th><th class="num">Go proxy $</th><th class="num">Go allowance $</th><th class="num">Contribution</th></tr></thead><tbody id="rows"></tbody></table></div></div>
<div class="foot"><p><strong>Coverage.</strong> This page includes Go models for which the current free Artificial Analysis v4.3 feed exposes both an Intelligence Index and a cost-per-task value. GPT 5.6 Luna, MiniMax M3/M2.7, and base MiMo-V2.5 are listed by OpenCode but were not plotted because the current AA feed did not expose a matching cost-per-task row at refresh time. Scores and prices can change; regenerate from the vendored refresh script.</p></div>
<script>__CHART__
const DATA=__DATA__;const fmt=(n,d=4)=>n<.001?n.toExponential(2):n.toFixed(d);const sorted=[...DATA].sort((a,b)=>a.usage_pct-b.usage_pct);let best=-Infinity;const frontier=[];for(const d of sorted){if(d.ii>best){frontier.push(d);best=d.ii}};
document.getElementById('kpis').innerHTML=[['Models plotted',DATA.length,'with AA task cost'],['Highest II',Math.max(...DATA.map(d=>d.ii)).toFixed(1),'latest v__VERSION__'],['Cheapest share',fmt(Math.min(...DATA.map(d=>d.usage_pct)),6)+'%','one benchmark task'],['Frontier points',frontier.length,'non-dominated models']].map(x=>`<div class="kpi"><div class="klabel">${x[0]}</div><div class="kvalue">${x[1]}</div><div class="knote">${x[2]}</div></div>`).join('');
const fset=new Set(frontier.map(d=>d.model));document.getElementById('rows').innerHTML=[...DATA].sort((a,b)=>b.ii-a.ii).map(d=>`<tr class="${fset.has(d.model)?'frontier':''}"><td><strong>${d.model}</strong></td><td>${d.aa_name}</td><td class="num">${d.ii.toFixed(1)}</td><td class="num">$${d.aa_task_cost.toFixed(4)}</td><td class="num">$${fmt(d.go_proxy_cost,6)}</td><td class="num">$${d.go_quota}</td><td class="num">${d.usage_pct.toFixed(4)}%</td></tr>`).join('');
const pts=DATA.map(d=>({x:d.usage_pct,y:d.ii,d}));new Chart(document.getElementById('chart'),{type:'scatter',data:{datasets:[{label:'Models',data:pts,backgroundColor:'#0969da',pointRadius:5,pointHoverRadius:7},{label:'Frontier',data:frontier.map(d=>({x:d.usage_pct,y:d.ii})),showLine:true,borderColor:'#1a7f37',backgroundColor:'#1a7f37',pointRadius:4,borderWidth:2,order:0}]},options:{responsive:true,maintainAspectRatio:false,scales:{x:{type:'linear',title:{display:true,text:'OpenCode Go monthly usage contribution (%)'},ticks:{callback:v=>v+'%'}},y:{title:{display:true,text:'Artificial Analysis Intelligence Index (v__VERSION__)'}}},plugins:{tooltip:{callbacks:{label:c=>{const d=c.raw.d;return d?`${d.model}: II ${d.ii}, ${d.usage_pct.toFixed(4)}% of Go allowance`:''}}}}}});
</script></div>
'''
def main():
 d=json.loads(DATA.read_text()); chart=CHART.read_text().split('//# sourceMappingURL=')[0]; page=TEMPLATE.replace('__DATA__',json.dumps(d['rows'])).replace('__VERSION__',d['aa_index_version']).replace('__DATE__',d['pulled_at'][:10]).replace('__CHART__',chart); PAGE.write_text(page); print(f'wrote {PAGE} ({len(d["rows"])} models)')
if __name__=='__main__':main()
