---
layout: single
title: "The Quant Quality Ladder"
date: 2026-08-29 00:00:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

# The Quant Quality Ladder

Someone ran the experiment I keep hoping to see. [@superalesha](https://x.com/superalesha/status/2093074966476713987) spent 1,351 hours of rented Blackwell time on the same model, [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), in nine versions: the BF16 reference plus eight quantized checkpoints from vLLM and llama.cpp, tested across 300 frozen tasks and 17,555 generations with reasoning turned up to maximum, about 91.4M reasoning tokens in total. The bill came to roughly $100 of GPU rental. This is the kind of benchmark people usually replace with a guess, and he went and ran it properly.

The chart below is the ladder he got. Hover a bar for the details, and use the toggle to hide the collapsed version so you can see how flat the plateau actually is.

<figure id="qql" class="qql">
<figcaption class="qql-cap"><strong>Pass rate by quantization, Qwen3.8-27B, xhigh thinking</strong> · 300 frozen tasks, 17,555 generations · shaded band: BF16 reference ± noise</figcaption>
<div class="qql-plot"><canvas id="qqlChart" role="img" aria-label="Bar chart of pass rates across eight quantizations of Qwen3.8-27B, showing a plateau near 80 percent and a collapse at 1.8 bits"></canvas></div>
<div class="qql-chips">
<button type="button" class="qql-chip is-on" data-view="all">All versions</button>
<button type="button" class="qql-chip" data-view="plateau">Plateau only</button>
</div>
<table class="qql-table">
<thead><tr><th>Version</th><th>Bits</th><th>Pass rate</th><th>vs best</th></tr></thead>
<tbody id="qqlRows"></tbody>
</table>
<p class="qql-note">Data from <a href="https://x.com/superalesha/status/2093074966476713987">@superalesha's 1,351-hour benchmark of Qwen3.8-27B</a>.</p>
</figure>

<style>
.qql{max-width:760px;margin:2em auto}
.qql-cap{font-size:.95em;text-align:center;margin-bottom:.6em;color:#1f2937}
.qql-plot{position:relative;height:440px}
.qql-chips{display:flex;gap:.5em;justify-content:center;margin:.8em 0}
.qql-chip{border:1px solid #d1d5db;background:#fff;color:#374151;border-radius:999px;padding:.35em 1em;font-size:.85em;cursor:pointer}
.qql-chip:hover{border-color:#2563eb;color:#2563eb}
.qql-chip.is-on{background:#2563eb;border-color:#2563eb;color:#fff}
.qql-table{width:100%;border-collapse:collapse;font-size:.9em;margin:.6em 0 0}
.qql-table th,.qql-table td{border-bottom:1px solid #e5e7eb;padding:.45em .6em;text-align:right}
.qql-table th:first-child,.qql-table td:first-child,.qql-table th:nth-child(2),.qql-table td:nth-child(2){text-align:left}
.qql-table th{color:#6b7280;font-weight:600}
.qql-table tr.cliff td{color:#dc2626;font-weight:600}
.qql-note{font-size:.8em;color:#6b7280;text-align:center;margin-top:.6em}
@media (max-width:480px){.qql-plot{height:380px}}
</style>

<script src="/assets/js/chart.umd.js"></script>
<script>
(function () {
  var RAW = [
    {fmt: "vLLM", label: "vLLM W4A16", bits: "4.25 (W4A16)", rate: 81.9},
    {fmt: "vLLM", label: "vLLM 4.25", bits: "4.25", rate: 81.4},
    {fmt: "vLLM", label: "vLLM 8", bits: "8", rate: 81.3},
    {fmt: "llama.cpp", label: "GGUF 6.5", bits: "6.5", rate: 80.8},
    {fmt: "llama.cpp", label: "GGUF ~4", bits: "~4", rate: 80.3},
    {fmt: "llama.cpp", label: "GGUF 3.6", bits: "3.6", rate: 79.9},
    {fmt: "llama.cpp", label: "GGUF 4.8", bits: "4.8", rate: 79.6},
    {fmt: "llama.cpp", label: "GGUF 2.7", bits: "2.7", rate: 79.4},
    {fmt: "llama.cpp", label: "GGUF IQ1_M", bits: "1.8 (IQ1_M)", rate: 43.0}
  ];
  var REF_LO = 79.4, REF_HI = 81.9;
  var best = RAW[0].rate;

  var tbody = document.getElementById("qqlRows");
  RAW.forEach(function (r, i) {
    var tr = document.createElement("tr");
    if (r.rate < 50) tr.className = "cliff";
    var delta = (r.rate - best).toFixed(1);
    tr.innerHTML = "<td>" + r.fmt + "</td><td>" + r.bits + "</td><td>" + r.rate.toFixed(1) + "%</td><td>" + (i === 0 ? "best" : delta) + "</td>";
    tbody.appendChild(tr);
  });

  var bandPlugin = {
    id: "band",
    afterDatasetsDraw: function (ch) {
      var ctx = ch.ctx, xa = ch.scales.x;
      var x1 = xa.getPixelForValue(REF_LO), x2 = xa.getPixelForValue(REF_HI);
      var top = ch.chartArea.top, bot = ch.chartArea.bottom;
      ctx.save();
      ctx.fillStyle = "rgba(148,163,184,0.14)";
      ctx.fillRect(x1, top, x2 - x1, bot - top);
      ctx.strokeStyle = "#94a3b8";
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(x1, top); ctx.lineTo(x1, bot);
      ctx.moveTo(x2, top); ctx.lineTo(x2, bot);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.restore();
    }
  };

  var valueLabels = {
    id: "values",
    afterDatasetsDraw: function (ch) {
      var ctx = ch.ctx, xa = ch.scales.x;
      ctx.save();
      ctx.font = "600 12px -apple-system, Segoe UI, sans-serif";
      ctx.textBaseline = "middle";
      ch.data.datasets[0].data.forEach(function (pt, i) {
        if (pt === null) return;
        var meta = ch.getDatasetMeta(0).data[i];
        if (!meta || !meta.skip) {
          ctx.fillStyle = pt.row.rate < 50 ? "#dc2626" : "#2563eb";
          ctx.textAlign = "left";
          ctx.fillText(pt.row.rate.toFixed(1) + "%", xa.getPixelForValue(pt.x) + 6, meta.y);
        }
      });
      ctx.restore();
    }
  };

  var colors = RAW.map(function (r) { return r.rate < 50 ? "#dc2626" : "#2563eb"; });
  var fullData = RAW.map(function (r) { return {x: r.rate, y: r.label, row: r}; });
  var ctx = document.getElementById("qqlChart").getContext("2d");
  var chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: RAW.map(function (r) { return r.label; }),
      datasets: [{
        data: fullData.slice(),
        backgroundColor: colors,
        borderRadius: 4,
        barThickness: 26
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {display: false},
        tooltip: {
          backgroundColor: "#111827",
          callbacks: {
            label: function (item) {
              var r = item.raw.row;
              return r.rate.toFixed(1) + "% pass · " + r.fmt + " · " + r.bits + " bits";
            },
            afterLabel: function (item) {
              var d = (item.raw.row.rate - best).toFixed(1);
              return d === "0.0" ? "reference for the ladder" : d + " points vs best";
            }
          }
        }
      },
      scales: {
        x: {
          min: 0, max: 90,
          ticks: {callback: function (v) { return v + "%"; }, color: "#6b7280"},
          grid: {color: "#eef1f5"}
        },
        y: {ticks: {color: "#374151", font: {size: 12}}, grid: {display: false}}
      }
    },
    plugins: [bandPlugin, valueLabels]
  });

  var chips = document.querySelectorAll(".qql-chip");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (c) { c.classList.remove("is-on"); });
      chip.classList.add("is-on");
      var plateau = chip.getAttribute("data-view") === "plateau";
      var keep = plateau ? RAW.filter(function (r) { return r.rate >= 50; }) : RAW;
      chart.data.labels = keep.map(function (r) { return r.label; });
      chart.data.datasets[0].data = keep.map(function (r) { return {x: r.rate, y: r.label, row: r}; });
      chart.options.scales.x.min = plateau ? 70 : 0;
      chart.options.scales.x.max = plateau ? 95 : 90;
      chart.update();
    });
  });

  window.__qqlChart = chart;
})();
</script>

The verdict is a ladder. Seven of the eight quants land inside the noise of the BF16 reference: vLLM's W4A16 build (4-bit weights, 16-bit activations) at 81.9%, its plain 4.25-bit and 8-bit siblings at 81.4% and 81.3%, then the llama.cpp family at 80.8, 80.3, 79.9, 79.6 and 79.4% down to 2.7 bits. The entire practical range of quantization costs about two and a half points. Then the cliff: GGUF IQ1_M at 1.8 bits collapses to 43.0%, a 37.3-point drop at p under 0.0001. What strikes me is the shape. Between 2.7 and 1.8 bits the model falls off a cliff, and nobody tested what happens in between.

I trust these numbers more than the average quant post because of the thinking setting. With xhigh reasoning across hundreds of tasks, weight errors get room to compound over long generations, which is exactly where quantization damage shows up. Simple benchmarks can smile at a broken model. Long reasoning chains do not.

For deployment the message is generous. Quantize this model down to 2.7 bits, leave a little margin, and spend your worry budget elsewhere. vLLM's quants edge out llama.cpp at comparable bit depths, but by fractions of a point, and that is not a reason to choose a serving stack. The range people keep landing on, 3 to 4 bits, sits deep inside the plateau.

The caveat is that one model is one model. Different models probably degrade at different rates. [OpenAI's scaling laws for precision](https://arxiv.org/abs/2411.04330) measured the underlying pattern: post-training quantization loss shrinks as models get bigger and grows with the amount of training data, so a 7B dense model and a 235B MoE will trace different ladders at the same bit depth. Architecture reshapes the picture as well. [MxMoE](https://arxiv.org/abs/2505.05799) found that individual layers inside a model vary wildly in how much precision they need, and experts in an MoE quantize unevenly, which is a problem dense models do not have. Even the family reputation matters. [Kaitchup's early notes](https://kaitchup.substack.com/p/qwen35-medium-models-dense-vs-moe) call the Qwen line unusually robust to aggressive low-bit quantization, while IQ1-class quants have collapsed on plenty of other models in the community benchmarks. The plateau-and-cliff shape is probably universal. The cliff position is not.

Which makes this benchmark the real asset. 300 frozen tasks, high reasoning, one reference, eight quants, roughly $100. Run the same ladder on the next model you plan to ship and you will know exactly where its cliff sits, instead of finding out after it is serving. That is a cheap insurance policy for a year when quantized models are quietly becoming the default way we run things on our own hardware.