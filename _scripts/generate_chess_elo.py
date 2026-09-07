#!/usr/bin/env python3
"""Generate the chess FIDE Elo project page and its compact data asset.

Input: _scripts/data/chess_elo/top100_YYYY-MM.csv (rank,name,fed,rating).
The vendored snapshots currently cover 2001-01 through 2026-09.  The page
keeps raw FIDE ratings separate from a peer-relative series:
rating - that list's top-100 mean, shifted to the latest top-100 mean.
"""
from __future__ import annotations
import csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "_scripts/data/chess_elo"
ASSET = ROOT / "assets/js/chess-elo-data.js"
PAGE = ROOT / "_pages/chess-elo.html"

files = sorted(INPUT.glob("top100_????-??.csv"))
if not files:
    raise SystemExit(f"No snapshots in {INPUT}")
dates=[]; means=[]; by_name={}
for path in files:
    date=path.stem.removeprefix("top100_")
    rows=[]
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["rating"]=int(row["rating"]); row["rank"]=int(row["rank"])
            row["name"]={"Kasparov, Gary":"Kasparov, Garry"}.get(row["name"],row["name"])
            rows.append(row)
    rows.sort(key=lambda r:r["rank"])
    dates.append(date); means.append(round(sum(r["rating"] for r in rows)/len(rows), 3))
    for r in rows:
        p=by_name.setdefault(r["name"], {"name":r["name"],"fed":r["fed"],"series":[]})
        p["series"].append([date,r["rating"],r["rank"]])
ref=means[-1]
for p in by_name.values():
    vals=[x[1] for x in p["series"]]
    i=max(range(len(vals)), key=vals.__getitem__)
    # Calibrated series is calculated in the browser from the per-list mean.
    j=dates.index(p["series"][i][0])
    p["peak"]={"date":p["series"][i][0],"rating":vals[i],"rank":p["series"][i][2],"calibrated":round(vals[i]-means[j]+ref,3)}
players=sorted(by_name.values(), key=lambda p:(-p["peak"]["rating"],p["name"]))
data={"dates":dates,"means":means,"referenceMean":ref,"players":list(players),"coverage":{"start":dates[0],"end":dates[-1],"lists":len(files),"players":len(players),"source":"Community FIDE-list mirrors: Anuj Dahiya (2001-2019) and 2700chess (2020-present)","shortLists":["2020-04","2020-05"]}}
ASSET.parent.mkdir(parents=True,exist_ok=True)
ASSET.write_text("window.CHESS_ELO_DATA = " + json.dumps(data,separators=(",",":"),ensure_ascii=False) + ";\n",encoding="utf-8")

front="""---
layout: single
title: \"Chess FIDE Elo Explorer\"
classes: wide
author_profile: false
permalink: /projects/chess-elo/
---"""
# The generated page is deliberately dependency-free: SVG keeps this project usable offline.
template=r'''<!DOCTYPE html>
<html lang="en" data-theme="light"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Chess FIDE Elo Explorer</title></head><body>
<div id="chess-app"><style>
#chess-app{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",sans-serif;color:#1f2328;line-height:1.5}#chess-app h1{font-size:1.55rem;margin-top:0}#chess-app .sub{color:#57606a;margin-top:-.5rem}.panel{background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;padding:1rem;margin:0 0 1rem}.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:.7rem}.kpi{background:#fff;border:1px solid #d0d7de;border-radius:7px;padding:.6rem .8rem}.k-label{color:#57606a;font-size:.72rem;text-transform:uppercase}.k-value{font-weight:650;font-size:1.12rem}.controls{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:.5rem 0}.controls button,.controls select,.controls input{font:inherit;font-size:.85rem;padding:.35rem .55rem;border:1px solid #d0d7de;border-radius:6px;background:#fff}.controls button.active{background:#0969da;color:#fff;border-color:#0969da}.chart{height:430px;background:#fff;border:1px solid #d0d7de;border-radius:7px;overflow:hidden}.chart svg{width:100%;height:100%}.legend{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.6rem}.legend button{border:1px solid #d0d7de;background:#fff;border-radius:100px;padding:.2rem .55rem;cursor:pointer}.legend button.off{color:#8c959f;text-decoration:line-through}.note,.muted{color:#57606a;font-size:.86rem}.table-wrap{overflow:auto;max-height:500px}.table{width:100%;border-collapse:collapse;font-size:.88rem}.table th,.table td{padding:.42rem .55rem;border-bottom:1px solid #d8dee4;text-align:left;white-space:nowrap}.table th{position:sticky;top:0;background:#f6f8fa}.num{text-align:right!important;font-variant-numeric:tabular-nums}.warning{border-left:4px solid #bf8700;background:#fff8c5;padding:.7rem .9rem}.sources{font-size:.88rem}.sources li{margin:.35rem 0}@media(max-width:700px){.chart{height:330px}}
</style>
<h1>Chess FIDE Elo Explorer</h1><p class="sub">Raw FIDE ratings and peer-calibrated ratings, monthly top-100 lists</p>
<div class="warning"><strong>Coverage warning.</strong> This verified snapshot set covers <span id="coverage"></span>. FIDE's official historical series begins in July 1971; the accessible mirror used here begins in January 2001, so 1971–2000 is not represented. This is not an all-time leaderboard.</div>
<div class="kpis" id="kpis"></div>
<div class="panel"><h2>Player trajectories</h2><div class="controls"><label for="search">Add player </label><input id="search" type="search" placeholder="e.g. Carlsen, Ding" autocomplete="off"><select id="matches" aria-label="Player search results" hidden></select><button class="mode active" data-mode="raw">Raw rating</button><button class="mode" data-mode="cal">Peer-calibrated</button></div><p class="muted">Peer-calibrated = player's rating minus that list's top-100 average, shifted to the latest list's average. It compares standing within the observed elite pool, not strength against an external era model.</p><div class="chart"><svg id="chart" viewBox="0 0 900 430" role="img" aria-label="Chess rating trajectories"></svg></div><div class="legend" id="legend"></div><p class="note" id="chart-note"></p></div>
<div class="panel"><h2>Top 20 peaks in the observed data</h2><p class="muted">Ordered by highest raw FIDE rating observed in these lists. Peak month is the month of that player's maximum in this coverage window.</p><div class="table-wrap"><table class="table"><thead><tr><th>#</th><th>Player</th><th>Fed.</th><th>Peak month</th><th class="num">Raw peak</th><th class="num">Peer-calibrated</th></tr></thead><tbody id="top"></tbody></table></div></div>
<div class="panel sources"><h2>Sources and method</h2><ul><li><strong>Input.</strong> The 2001–September 2019 standard-list snapshots come from the community-maintained <a href="https://github.com/anujdahiya24/FIDE">Anuj Dahiya FIDE mirror</a>. January 2020–September 2026 comes from monthly top-100 snapshots at <a href="https://2700chess.com/fide-top100-history">2700chess</a>, a secondary mirror of FIDE lists. These are labelled as mirrors, not presented as direct official-FIDE downloads.</li><li><strong>Official history.</strong> FIDE's standard rating list series starts in July 1971. The accessible dataset used here begins in 2001, so 1971–2000 remains a data gap. No Chessmetrics or Edo ratings are mixed into this FIDE-based series.</li><li><strong>Calibration.</strong> For every list, calculate the mean rating of the listed elite field. A player's calibrated value is raw rating − that list's mean + the latest list's mean. This is a peer-relative location adjustment, not a claim that historical FIDE ratings are directly comparable across every era.</li><li><strong>Limitations.</strong> Only players appearing in a supplied top-100 list are represented. The archive has uneven historical intervals before 2013, list methodology changes, federation/name changes, and the incomplete 1971–2000 archive affect comparisons. Peak values are peaks within the stated coverage.</li></ul></div>
<script src="/assets/js/chess-elo-data.js"></script><script>(function(){const D=window.CHESS_ELO_DATA,players=D.players,dates=D.dates,means=D.means;const colors=['#0969da','#cf222e','#1a7f37','#8250df','#9a6700','#0550ae','#d1242f','#116329','#bc4c00','#563d7c'];let mode='raw',selected=players.slice(0,3).map(p=>p.name),off=new Set();const $=id=>document.getElementById(id);$('coverage').textContent=D.coverage.start+' through '+D.coverage.end;[['Lists',D.coverage.lists],['Players',D.coverage.players],['Latest top-100 mean',D.referenceMean],['Months',dates.length]].forEach(x=>{$('kpis').innerHTML+=`<div class="kpi"><div class="k-label">${x[0]}</div><div class="k-value">${x[1]}</div></div>`});const esc=s=>s.replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));function p(name){return players.find(x=>x.name===name)}function val(x,i){const j=dates.indexOf(x.series[i][0]);return mode==='raw'?x.series[i][1]:x.series[i][1]-means[j]+D.referenceMean}function render(){const svg=$('chart'),W=900,H=430,L=58,R=18,T=18,B=42,all=selected.flatMap(n=>{let x=p(n);return x?x.series.map((_,i)=>val(x,i)):[]});let lo=Math.floor(Math.min(...all)/50)*50,hi=Math.ceil(Math.max(...all)/50)*50;if(hi===lo)hi+=100;const X=i=>L+i*(W-L-R)/(dates.length-1),Y=v=>T+(hi-v)*(H-T-B)/(hi-lo);let out='';for(let v=lo;v<=hi;v+=50)out+=`<line x1="${L}" x2="${W-R}" y1="${Y(v)}" y2="${Y(v)}" stroke="#d8dee4"/><text x="${L-8}" y="${Y(v)+4}" text-anchor="end" font-size="11" fill="#57606a">${v}</text>`;dates.forEach((d,i)=>{if(i%Math.ceil(dates.length/8)===0)out+=`<text x="${X(i)}" y="${H-12}" text-anchor="middle" font-size="11" fill="#57606a">${d}</text>`});selected.forEach((n,k)=>{let x=p(n);if(!x||off.has(n))return;let pts=x.series.map((q,i)=>`${X(dates.indexOf(q[0]))},${Y(val(x,i))}`).join(' ');out+=`<polyline points="${pts}" fill="none" stroke="${colors[k%colors.length]}" stroke-width="2.4"/>`});svg.innerHTML=out;$('chart-note').textContent=(mode==='raw'?'Raw FIDE rating':'Peer-calibrated rating')+'; monthly observations are connected within each player series.';$('legend').innerHTML=selected.map((n,k)=>`<button class="${off.has(n)?'off':''}" data-name="${esc(n)}" style="border-color:${colors[k%colors.length]}">${esc(n)} ${off.has(n)?'(hidden)':''}</button>`).join('');$('legend').querySelectorAll('button').forEach(b=>b.onclick=()=>{let n=b.dataset.name;off.has(n)?off.delete(n):off.add(n);render()})}function add(n){if(!selected.includes(n)){selected.push(n);off.delete(n);render()}}const s=$('search'),m=$('matches');s.oninput=()=>{let q=s.value.toLowerCase();let hits=q.length>1?players.filter(x=>x.name.toLowerCase().includes(q)).slice(0,12):[];m.innerHTML=hits.map(x=>`<option>${esc(x.name)}</option>`).join('');m.hidden=!hits.length};m.onchange=()=>{add(m.value);s.value='';m.hidden=true};document.querySelectorAll('.mode').forEach(b=>b.onclick=()=>{document.querySelectorAll('.mode').forEach(x=>x.classList.remove('active'));b.classList.add('active');mode=b.dataset.mode;render()});$('top').innerHTML=players.slice(0,20).map((x,i)=>`<tr><td>${i+1}</td><td>${esc(x.name)}</td><td>${esc(x.fed)}</td><td>${x.peak.date}</td><td class="num">${x.peak.rating}</td><td class="num">${x.peak.calibrated}</td></tr>`).join('');render()})()</script></div></body></html>'''
page=front+'\n\n'+template.replace('__DATA__','window.CHESS_ELO_DATA = '+json.dumps(data,separators=(',',':'),ensure_ascii=False)+';')
PAGE.write_text(page,encoding='utf-8')
print(f"wrote {ASSET} ({ASSET.stat().st_size} bytes), {PAGE} ({PAGE.stat().st_size} bytes), {len(files)} lists, {len(players)} players")
