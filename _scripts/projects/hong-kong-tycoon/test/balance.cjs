/* Deterministic policy experiments, not a claim of optimal human play. */
const E = require('../engine.js');
function campaign(seed, policy) {
  let s = E.act(E.newGame(seed), { type: 'establish' });
  while (!s.ending && !s.distress) {
    for (const good of Object.keys(E.GOODS)) {
      if (s.stock[good]) s = E.act(s, { type: 'sell', good, qty: s.stock[good] });
    }
    if (policy === 'civic' && s.plots.some(p => p.built)) {
      if (!s.manager && s.cash > 170000) s = E.act(s, { type: 'manager' });
      if (E.activeProjects(s) < (s.manager ? 2 : 1)) {
        const tender = [...s.tenders].sort((a, b) => Number(b.major) - Number(a.major)).find(c => s.official >= c.requirement && s.cash > c.bond + E.commitments(s) + E.contractCost(s, c).cash + 35000);
        if (tender) s = E.act(s, { type: 'contract', id: tender.id });
      }
    }
    const reserve = Math.max(20000, E.commitments(s) + 15000);
    const choices = policy === 'opium' ? ['opium', 'tea'] : ['tea'];
    for (const good of choices) {
      const qty = Math.min(good === 'opium' ? 22 : 90, Math.floor((s.cash - reserve) / E.buyQuote(s, good, 1)), Math.floor((E.capacity(s, true) - E.usedSpace(s)) / E.GOODS[good].space));
      if (qty > 0) s = E.act(s, { type: 'buy', good, qty });
    }
    s = E.act(s, { type: 'end' });
    E.validateSave(s);
  }
  return { ending: s.ending || 'distress', worth: E.netWorth(s), turn: s.turn, contracts: s.completed };
}
for (const policy of ['tea', 'opium', 'civic']) {
  const results = Array.from({ length: 100 }, (_, i) => campaign(`balance-${i}`, policy));
  const worths = results.map(r => r.worth).sort((a, b) => a - b);
  const endings = results.reduce((counts, r) => ({ ...counts, [r.ending]: (counts[r.ending] || 0) + 1 }), {});
  console.log(JSON.stringify({ policy, runs: results.length, endings, worth: { min: worths[0], median: worths[50], max: worths[99] }, meanEndTurn: results.reduce((n, r) => n + r.turn, 0) / 100 }));
}
