#!/usr/bin/env python3
"""Fetch AA v4.3 data and build the auditable OpenCode Go input dataset."""
import json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_scripts/data/opencode_go_frontier.json"
IDS = {
    "Grok 4.5":"794f69b5-cede-482b-b1cc-d769478497cd", "GLM-5.2":"f7a4ea75-e548-4069-80d4-9be8bc7c009b",
    "GLM-5.1":"5aa1c578-af76-4b91-8699-cdd43582b3af", "GPT 5.6 Luna":"426d24c8-49ae-482a-b4a8-20f1c53f21c1", "Kimi K3":"f7d2fc3e-1f7b-405f-818c-07952a4af78f",
    "Kimi K2.7 Code":"8d0cb231-7303-452c-9923-a9620b948475", "Kimi K2.6":"0de67206-4d36-4d10-b8f6-cf37fa747a03",
    "MiMo-V2.5-Pro":"00f1248e-78e3-4230-8dc8-5e13ba8645e2", "Qwen3.8 Max":"b112af07-3bd5-4647-b09f-b23204361bb2",
    "Qwen3.7 Max":"69534bed-2ffd-4235-832b-e20a810333ab", "Qwen3.7 Plus":"a87fce42-eea3-4e45-a96d-fe057814f371",
    "DeepSeek V4 Pro":"83173329-c09a-41f1-a028-a282a5f908d7", "DeepSeek V4 Flash":"fe4c0848-e284-4e52-a79d-cdc28392f1a9", "MiniMax M3":"277f939a-985b-4b37-859d-b3eabc7c0b26", "MiniMax M2.7":"4bbceacb-cf47-464b-b60f-e1d1fe016d67",
    "Hy3":"b23e6c69-96e5-44c9-8f58-4b42e0c399d5",
}
# OpenCode's published observed request pattern and Go price table.
GO = {
"Grok 4.5":(1100,71500,220,2,6,.30,15), "GLM-5.2":(700,52000,150,1.4,4.4,.26,60), "GLM-5.1":(700,52000,150,1.4,4.4,.26,60), "GPT 5.6 Luna":(1000,50000,220,.20,1.20,.02,15),
"Kimi K3":(1050,76500,300,3,15,.30,15), "Kimi K2.7 Code":(870,55000,200,.95,4,.19,60), "Kimi K2.6":(870,55000,200,.95,4,.16,60),
"MiMo-V2.5-Pro":(790,86000,305,.435,.87,.003625,15), "Qwen3.8 Max":(420,66000,200,2,6,.25,15),
"Qwen3.7 Max":(420,66000,200,2.5,7.5,.50,60), "Qwen3.7 Plus":(500,57000,190,.4,1.6,.04,60),
"DeepSeek V4 Pro":(750,82000,290,.435,.87,.003625,15), "DeepSeek V4 Flash":(790,68000,280,.14,.28,.0028,60), "MiniMax M3":(510,56000,190,.30,1.20,.06,60), "MiniMax M2.7":(300,55000,125,.30,1.20,.06,60),
"Hy3":(830,71500,295,.14,.58,.035,60),
}
def fetch():
    key=os.environ["ARTIFICIAL_ANALYSIS_API"]; models=[]
    for page in range(1,5):
        url=f"https://artificialanalysis.ai/api/v2/language/models/free?tier=free&intelligence_index_version=4.3&page={page}&page_size=200"
        req=urllib.request.Request(url, headers={"x-api-key":key})
        with urllib.request.urlopen(req, timeout=60) as r: models += json.load(r)["data"]
    return {m["id"]:m for m in models}
def main():
    models=fetch(); rows=[]
    for model, mid in IDS.items():
        m=models[mid]; cfg=GO[model]; inp,cache,out,gi,go,gc,quota=cfg
        aa=m["pricing"]; task=m["artificial_analysis_intelligence_index_cost"]["cost_per_task"]["total_cost"]
        # AA task cost is at its published 3:1 input/output price ratio. Scale it
        # by the effective Go price for Go's observed cached-request pattern.
        aa_blended=(3*aa["price_1m_input_tokens"]+aa["price_1m_output_tokens"])/4
        go_effective=(inp*gi+cache*gc+out*go)/1_000_000
        proxy=task*go_effective/aa_blended
        rows.append({"model":model,"aa_name":m["name"],"creator":m["model_creator"]["name"],"ii":m["evaluations"]["artificial_analysis_intelligence_index"],"aa_task_cost":task,"aa_input_price":aa["price_1m_input_tokens"],"aa_output_price":aa["price_1m_output_tokens"],"go_input_tokens":inp,"go_cached_tokens":cache,"go_output_tokens":out,"go_input_price":gi,"go_cached_price":gc,"go_output_price":go,"go_quota":quota,"go_proxy_cost":round(proxy,8),"usage_pct":round(proxy/quota*100,6)})
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps({"pulled_at":datetime.now(timezone.utc).isoformat(),"aa_index_version":"4.3","rows":rows},indent=2)+"\n")
    print(f"wrote {OUT} ({len(rows)} models)")
if __name__ == "__main__": main()
