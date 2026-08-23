#!/usr/bin/env python3
"""Generate _pages/hk-rent-index.html (HK Private Domestic Rental Index explorer).

Source: RVD his_data_3.xls (Private Domestic - Rental Indices by Class,
Territory-Wide), extracted to _scripts/data/hk_rent_index_rvd.json.
Records: {y, m, freq: "M"|"Q", p?: true(provisional), A..E, ALL, ABC_lt100, DE_ge100}.

Deterministic: same input -> byte-identical page. Regenerate after refreshing
the data snapshot, commit both together.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "_scripts/data/hk_rent_index_rvd.json")))
CHARTJS = open(os.path.join(ROOT, "_scripts/vendor/chart.umd.js")).read()
DATA_JS = json.dumps(DATA, separators=(",", ":"))

TEMPLATE = r"""---
layout: single
title: "Hong Kong Rental Index Explorer"
classes: wide
author_profile: false
permalink: /projects/hk-rent-index/
---

<div id="hri-app">
<style>
#hri-app { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif; color:#1f2328; line-height:1.5; }
#hri-app .sub { color:#57606a; margin:0 0 1rem; font-size:.95rem; }
#hri-app .kpis { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:.75rem; margin-bottom:1.25rem; }
#hri-app .kpi { background:#f6f8fa; border:1px solid #d0d7de; border-radius:8px; padding:.7rem .9rem; }
#hri-app .kpi .k-label { font-size:.72rem; text-transform:uppercase; letter-spacing:.04em; color:#57606a; }
#hri-app .kpi .k-value { font-size:1.15rem; font-weight:600; margin-top:.15rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
#hri-app .kpi .k-note { font-size:.78rem; color:#57606a; }
#hri-app .pos { color:#1a7f37; } #hri-app .neg { color:#cf222e; } #hri-app .warn { color:#9a6700; }
#hri-app .panel { background:#f6f8fa; border:1px solid #d0d7de; border-radius:8px; padding:.9rem 1rem; margin-bottom:1.25rem; }
#hri-app h2 { font-size:1.05rem; margin:0 0 .6rem; border-bottom:none; padding-bottom:0; }
#hri-app .controls { display:flex; flex-wrap:wrap; gap:.5rem .6rem; align-items:center; margin-bottom:.75rem; }
#hri-app .ctl-label { font-size:.8rem; color:#57606a; font-weight:600; }
#hri-app button.pill { font-size:.8rem; padding:.3rem .8rem; border:1px solid #d0d7de; background:#fff; color:#57606a; border-radius:100px; cursor:pointer; }
#hri-app button.pill.active { background:#0969da; border-color:#0969da; color:#fff; }
#hri-app select.sel { font-size:.85rem; padding:.25rem .4rem; border:1px solid #d0d7de; border-radius:6px; background:#fff; color:#1f2328; max-width:9.5rem; }
#hri-app .chart-wrap { position:relative; height:400px; background:#fff; border:1px solid #d0d7de; border-radius:8px; padding:.5rem; }
#hri-app .rebase-note { font-size:.8rem; color:#656d76; margin-top:.5rem; }
#hri-app ul.reading li { margin-bottom:.35rem; font-size:.92rem; color:#57606a; }
@media(max-width:700px){ #hri-app .chart-wrap{height:320px;} }
</style>

<h1 style="margin-top:0;">Hong Kong Private Domestic Rental Index</h1>
<p class="sub">Rating &amp; Valuation Department &bull; published base 1999 = 100 &bull; monthly from Jan 1993, quarterly before &bull; latest month provisional</p>

<div class="kpis" id="hri-kpis"></div>

<div class="panel">
  <h2>Index explorer</h2>
  <div class="controls">
    <span class="ctl-label">Period:</span>
    <button class="pill preset active" data-preset="all">All (1979&ndash;)</button>
    <button class="pill preset" data-preset="20">20Y</button>
    <button class="pill preset" data-preset="15">15Y</button>
    <button class="pill preset" data-preset="10">10Y</button>
    <button class="pill preset" data-preset="5">5Y</button>
    <span style="margin-left:auto;"></span>
    <span class="ctl-label">From</span> <select class="sel" id="hri-from"></select>
    <span class="ctl-label">To</span> <select class="sel" id="hri-to"></select>
  </div>
  <div class="controls" id="hri-series"></div>
  <div class="chart-wrap"><canvas id="hri-chart"></canvas></div>
  <div class="rebase-note" id="hri-note"></div>
</div>

<div class="panel">
  <h2>Reading the index</h2>
  <ul class="reading">
    <li><strong>1979&ndash;1981:</strong> rents roughly doubled in three years in the early-80s boom.</li>
    <li><strong>1982&ndash;1985:</strong> correction and stabilisation around the Joint Declaration years.</li>
    <li><strong>1985&ndash;1997:</strong> the long pre-handover run-up; the index roughly quadrupled.</li>
    <li><strong>1998&ndash;2003:</strong> Asian Financial Crisis into SARS &mdash; the deepest rent decline on record, troughing in mid-2003.</li>
    <li><strong>2004&ndash;2019:</strong> sixteen years of nearly uninterrupted growth to the Aug 2019 cyclical peak.</li>
    <li><strong>2020&ndash;2021:</strong> pandemic-era correction of roughly 9% off peak despite low rates.</li>
    <li><strong>2022&ndash;2026:</strong> recovery on talent inflows; Jun 2026 sets a fresh all-time high (provisional).</li>
  </ul>
</div>

<div class="panel">
  <h2>Methodology</h2>
  <ul class="reading">
    <li>Data: RVD historical statistics <em>his_data_3.xls</em>, "Private Domestic &mdash; Rental Indices by Class (Territory-Wide)". Retrieved August 2026.</li>
    <li>Classes are by saleable area: A under 40 m&#178;; B 40&ndash;69.9; C 70&ndash;99.9; D 100&ndash;159.9; E 160 or above. All Classes is the RVD aggregate.</li>
    <li>The chart is rebased for reading convenience: whatever window you pick, each series is rebased so its first available observation becomes 100, so lines show cumulative change within the window. (The All Classes aggregate begins 1980 Q3; classes A&ndash;E begin 1979 Q4.) The official series remains base 1999 = 100.</li>
    <li>Quarterly observations before Jan 1993 are plotted as-is at quarter start months. The most recent month is provisional and subject to revision.</li>
  </ul>
</div>

<script>__CHARTJS__</script>
<script>
const RAW = __DATA__;
const SERIES_DEF = [
  ["ALL","All Classes","#0969da"],
  ["A","Class A (<40m\u00B2)","#1a7f37"],
  ["B","Class B (40\u201370m\u00B2)","#9a6700"],
  ["C","Class C (70\u2013100m\u00B2)","#8250df"],
  ["D","Class D (100\u2013160m\u00B2)","#0598b0"],
  ["E","Class E (\u2265160m\u00B2)","#cf222e"]
];
let active = new Set(["ALL"]);
function ymOf(r){ return r.y*100+r.m; }
function labelOf(r){ return r.freq==="Q" ? r.y+" Q"+(Math.floor((r.m-1)/3)+1) : r.y+"-"+String(r.m).padStart(2,"0"); }

const fromSel=document.getElementById("hri-from"), toSel=document.getElementById("hri-to");
RAW.forEach((r,i)=>{ fromSel.add(new Option(labelOf(r),i)); toSel.add(new Option(labelOf(r),i)); });
fromSel.value=0; toSel.value=RAW.length-1;
let chart=null;

function render(){
  const a=+fromSel.value,b=+toSel.value, lo=Math.min(a,b), hi=Math.max(a,b);
  const rows=RAW.slice(lo,hi+1);
  const labels=rows.map(labelOf);
  const datasets=[];
  for(const [key,label,color] of SERIES_DEF){
    if(!active.has(key)) continue;
    // Rebase from the FIRST OBSERVATION AVAILABLE within the window. RVD's
    // All Classes aggregate starts 1980 Q3 (classes A-E start 1979 Q4), so
    // rebasing off rows[0] blindly yields undefined/null -> invisible line.
    let base=null,bi=-1;
    for(let i=0;i<rows.length;i++){ if(rows[i][key]!=null){ base=rows[i][key]; bi=i; break; } }
    let last=null;
    const data=rows.map((r,i)=>{
      if(base==null||i<bi) return null;
      if(r[key]==null) return last;
      last=+(r[key]/base*100).toFixed(1); return last;
    });
    datasets.push({label,data,borderColor:color,backgroundColor:color+"22",
      tension:.25,pointRadius:rows.length>150?0:2,pointHoverRadius:5,borderWidth:2.5,spanGaps:true});
  }
  if(chart) chart.destroy();
  chart=new Chart(document.getElementById("hri-chart"),{
    type:"line",data:{labels,datasets},
    options:{responsive:true,maintainAspectRatio:false,
      interaction:{mode:"index",intersect:false},
      plugins:{legend:{labels:{color:"#57606a"}},
        tooltip:{backgroundColor:"#ffffff",titleColor:"#1f2328",bodyColor:"#1f2328",
          borderColor:"#d0d7de",borderWidth:1,
          callbacks:{label:c=>" "+c.dataset.label+": "+c.parsed.y.toFixed(1)+" ("+(c.parsed.y-100>=0?"+":"")+(c.parsed.y-100).toFixed(1)+"% vs window start)"}}},
      scales:{x:{grid:{display:false},ticks:{color:"#656d76",maxTicksLimit:14}},
        y:{grid:{color:"rgba(208,215,222,.55)"},ticks:{color:"#656d76"}}}}
  });
  renderKpis(rows);
  document.getElementById("hri-note").textContent=
    "Window "+labelOf(rows[0])+" to "+labelOf(rows[rows.length-1])+
    " ("+rows.length+" observations) \u00B7 "+
    (SERIES_DEF.some(([k])=>active.has(k)&&rows[0][k]==null)
      ? "each series rebased: its first available observation = 100"
      : "rebased: "+labelOf(rows[0])+" = 100");
}

function renderKpis(rows){
  const firstR=rows[0],lastR=rows[rows.length-1];
  // First available value per key (ALL starts 1980 Q3; see render()).
  function firstVal(k){ for(const r of rows){ if(r[k]!=null) return r[k]; } return null; }
  function chg(k){ const f=firstVal(k); return (f!=null&&lastR[k]!=null)?(lastR[k]/f-1)*100:null; }
  let peak=null; rows.forEach(r=>{ if(r.ALL!=null&&(!peak||r.ALL>peak.v)) peak={lab:labelOf(r),v:r.ALL}; });
  const spanYears=((lastR.y-firstR.y)+(lastR.m-firstR.m)/12).toFixed(1);
  const fmt=v=>v==null?"n/a":(v>=0?"+":"")+v.toFixed(1)+"%";
  const cls=v=>v==null?"":(v>=0?"pos":"neg");
  document.getElementById("hri-kpis").innerHTML=`
    <div class="kpi"><div class="k-label">Latest (${labelOf(lastR)})</div><div class="k-value">${lastR.ALL!=null?lastR.ALL.toFixed(1):"n/a"}</div><div class="k-note">${lastR.p?"provisional":""}</div></div>
    <div class="kpi"><div class="k-label">Change over window</div><div class="k-value ${cls(chg("ALL"))}">${fmt(chg("ALL"))}</div><div class="k-note">rebased to 100 at ${firstVal("ALL")!=null?labelOf(rows.find(r=>r.ALL!=null)):labelOf(firstR)}</div></div>
    <div class="kpi"><div class="k-label">Peak in window</div><div class="k-value">${peak?peak.v.toFixed(1):"n/a"}</div><div class="k-note">${peak?peak.lab:""}</div></div>
    <div class="kpi"><div class="k-label">Window span</div><div class="k-value">${spanYears} yrs</div><div class="k-note">${rows.length} observations</div></div>`;
}

document.querySelectorAll("#hri-app .preset").forEach(btn=>{
  btn.addEventListener("click",()=>{
    document.querySelectorAll("#hri-app .preset").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    const p=btn.dataset.preset;
    if(p==="all"){ fromSel.value=0; }
    else{
      const lastY=RAW[RAW.length-1].y;
      let i=RAW.findIndex(r=>r.y>=lastY-(+p)+1); if(i<0)i=0;
      fromSel.value=i;
    }
    toSel.value=RAW.length-1; render();
  });
});
[fromSel,toSel].forEach(s=>s.addEventListener("change",()=>{
  document.querySelectorAll("#hri-app .preset").forEach(b=>b.classList.remove("active")); render();
}));
const bar=document.getElementById("hri-series");
for(const [key,label,color] of SERIES_DEF){
  const btn=document.createElement("button");
  btn.className="pill"+(active.has(key)?" active":"");
  btn.textContent=label;
  btn.style.borderColor=color;
  btn.style.background=active.has(key)?color:"#fff";
  btn.style.color=active.has(key)?"#fff":color;
  btn.addEventListener("click",()=>{
    if(active.has(key)){ if(active.size>1) active.delete(key);} else active.add(key);
    btn.style.background=active.has(key)?color:"#fff";
    btn.style.color=active.has(key)?"#fff":color;
    render();
  });
  bar.appendChild(btn);
}
render();
</script>
</div>
"""

html = TEMPLATE.replace("__CHARTJS__", CHARTJS).replace("__DATA__", DATA_JS)
out = os.path.join(ROOT, "_pages/hk-rent-index.html")
with open(out, "w") as f:
    f.write(html)
print("written", out, len(html), "chars")
