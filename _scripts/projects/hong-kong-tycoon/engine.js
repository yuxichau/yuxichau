/* The simulation has no DOM, clock, filesystem, or network dependencies. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.Tycoon = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const VERSION = 1;
  const SEASONS = ['Spring', 'Summer', 'Autumn', 'Winter'];
  const GOODS = {
    rice: { name: 'Rice', base: 200, margin: .18, space: 1, demand: 200, spoil: .035, description: 'A staple trade. Broad demand, modest returns, and perishable stock.' },
    tea: { name: 'Tea', base: 600, margin: .24, space: 1, demand: 95, spoil: .012, description: 'The export mainstay. Better margins, sensitive to overseas demand.' },
    cement: { name: 'Cement', base: 160, margin: .20, space: 2, demand: 140, spoil: 0, description: 'Bulky building material. Supply public works or sell into a building boom.' },
    opium: { name: 'Opium', base: 1800, margin: .43, space: 1, demand: 28, spoil: 0, description: 'High-value cargo. Theft, route enforcement, and lasting public distrust.' }
  };
  const LOCATIONS = {
    town: { name: 'Victoria town', price: 20000, freight: .045, exposure: 1, description: 'Balanced costs and weather exposure.' },
    waterfront: { name: 'Waterfront', price: 28000, freight: .025, exposure: 1.35, description: 'Cheaper handling; more exposed to storms.' },
    outskirts: { name: 'Outskirts', price: 14000, freight: .075, exposure: .7, description: 'Cheaper land; expensive cartage.' }
  };
  const PROJECTS = {
    wharf: { name: 'Public wharf', effect: 'handling', benefit: 'Port handling charges −8%', description: 'New landing stages shorten the journey from ship to store.' },
    roads: { name: 'Cartage road', effect: 'cartage', benefit: 'Cartage charges −8%', description: 'A surfaced road connects the merchants’ stores to the harbour.' },
    drainage: { name: 'Town drainage', effect: 'flood', benefit: 'Flood-related losses −8%', description: 'New drains protect cargo and reduce seasonal disruption.' },
    water: { name: 'Public waterworks', effect: 'labour', benefit: 'House operating costs −8%', description: 'Reliable water reduces illness and interruptions to work.' },
    market: { name: 'Market hall', effect: 'demand', benefit: 'Local market depth +8%', description: 'A covered market brings more buyers to the growing settlement.' }
  };
  const UPGRADES = {
    floors: { name: 'Raised floors', price: 6000, description: 'Stored-cargo storm losses reduced by 60%.' },
    ventilation: { name: 'Ventilation', price: 4500, description: 'Rice and tea spoilage reduced by 65%.' },
    dry: { name: 'Dry store', price: 4500, description: 'Cement damp losses reduced by 80%.' },
    security: { name: 'Watchmen', price: 5500, description: 'Opium theft risk reduced; $100 seasonal upkeep.' },
    expansion: { name: 'Warehouse extension', price: 12000, description: 'Adds 120 storage spaces.' }
  };
  const clone = value => JSON.parse(JSON.stringify(value));
  const clamp = (n, lo, hi) => Math.max(lo, Math.min(hi, n));
  const round = n => Math.round(n);
  const emptyGoods = () => Object.fromEntries(Object.keys(GOODS).map(k => [k, 0]));
  function random(s) {
    s.rng = (Math.imul(1664525, s.rng) + 1013904223) >>> 0;
    return s.rng / 4294967296;
  }
  function seedNumber(seed) {
    let h = 2166136261;
    for (const ch of String(seed)) h = Math.imul(h ^ ch.charCodeAt(0), 16777619);
    return h >>> 0;
  }
  function date(s) { return s.turn >= 72 ? 'Spring 1870' : `${SEASONS[s.turn % 4]} ${1852 + Math.floor(s.turn / 4)}`; }
  function record(s, text, tone = 'neutral') {
    s.log.unshift({ turn: s.turn, text, tone });
    s.log = s.log.slice(0, 160);
  }
  function standing(s, official, trust) {
    s.official = clamp(s.official + official, 0, 100);
    s.trust = clamp(s.trust + trust, 0, 100);
  }
  function reduction(s, effect) { return Math.min(.28, s.city[effect] * .08); }
  function capacity(s, projected = false) {
    return s.plots.reduce((n, p) => n + (p.built || (projected && p.building) ? 180 + (p.upgrades.includes('expansion') ? 120 : 0) : 0), 0);
  }
  function usedSpace(s) {
    return Object.entries(GOODS).reduce((n, [k, g]) => n + (s.stock[k] + s.incoming.filter(c => c.good === k).reduce((a, c) => a + c.qty, 0)) * g.space, 0);
  }
  function protection(s, upgrade) {
    const stores = s.plots.filter(p => p.built);
    return stores.length ? stores.filter(p => p.upgrades.includes(upgrade)).length / stores.length : 0;
  }
  function freight(s) {
    const stores = s.plots.filter(p => p.built || p.building);
    const base = stores.length ? stores.reduce((n, p) => n + LOCATIONS[p.location].freight, 0) / stores.length : .05;
    return .015 * (1 - reduction(s, 'handling')) + base * (1 - reduction(s, 'cartage'));
  }
  function operating(s) {
    const fixed = 1000 + s.plots.reduce((n, p) => n + p.price * .01 + (p.built ? 500 : 0) + (p.upgrades.includes('security') ? 100 : 0), 0) + (s.manager ? 650 : 0);
    return round(fixed * (1 - reduction(s, 'labour')) + usedSpace(s) * 1.5 + s.debt * .025);
  }
  function propertyValue(s) {
    return s.plots.reduce((n, p) => n + p.price + (p.built ? 15000 : p.building ? 10000 : 0) + p.upgrades.reduce((v, u) => v + UPGRADES[u].price, 0), 0);
  }
  function netWorth(s) {
    return round(s.cash - s.debt + propertyValue(s) + Object.keys(GOODS).reduce((n, k) => n + s.stock[k] * s.prices[k], 0) + s.incoming.reduce((n, c) => n + c.value, 0) + s.contracts.reduce((n, c) => n + c.bond, 0));
  }
  function creditLimit(s) {
    return round(propertyValue(s) * .45 + Object.keys(GOODS).reduce((n, k) => n + s.stock[k] * s.prices[k] * .25, 0) + (s.official >= 25 ? 10000 : 0));
  }
  function activeProjects(s) { return s.contracts.length + s.plots.filter(p => p.building).length; }
  function buyQuote(s, good, qty, insured = s.insurance) {
    return round(s.prices[good] * qty * (1 + freight(s) + (insured ? .03 : 0)));
  }
  function demand(s, good) { return Math.floor(GOODS[good].demand * (1 + s.turn * .012) * (1 + reduction(s, 'demand'))); }
  function sellQuote(s, good, qty) {
    const normal = Math.min(qty, Math.max(0, demand(s, good) - s.sold[good]));
    return round(s.prices[good] * (1 + GOODS[good].margin) * (normal + (qty - normal) * .78));
  }
  function contractCost(s, c) {
    const material = Math.min(s.stock.cement, c.cement);
    const shortfall = c.cement - material;
    return { cash: c.labour + buyQuote(s, 'cement', shortfall, false) * 1.12, cement: material, shortfall };
  }
  function commitments(s) { return operating(s) + s.contracts.reduce((n, c) => n + round(contractCost(s, c).cash), 0); }
  function eligible(s) {
    return s.turn >= 31 && s.official >= 75 && s.trust >= 60 && netWorth(s) >= 350000 && s.completed >= 4 && s.majorCompleted >= 2 && s.turn - s.lastOpium >= 8 && s.cash >= 0;
  }
  function appointment(s) {
    return [
      { label: 'Eight years established', current: Math.min(8, Math.floor(s.turn / 4)), target: 8, met: s.turn >= 32 },
      { label: 'Official Standing', current: s.official, target: 75, met: s.official >= 75 },
      { label: 'Public Trust', current: s.trust, target: 60, met: s.trust >= 60 },
      { label: 'Net worth', current: netWorth(s), target: 350000, met: netWorth(s) >= 350000, money: true },
      { label: 'Public contracts delivered', current: s.completed, target: 4, met: s.completed >= 4 },
      { label: 'Major projects delivered', current: s.majorCompleted, target: 2, met: s.majorCompleted >= 2 },
      { label: 'Seasons out of opium', current: Math.min(8, s.turn - s.lastOpium), target: 8, met: s.turn - s.lastOpium >= 8 },
      { label: 'Consecutive qualifying seasons', current: s.qualifying, target: 4, met: s.qualifying >= 4 }
    ];
  }
  function makeTender(s, type, major, index) {
    const stages = major ? 4 : 3;
    const cement = major ? 16 : 8;
    const labour = major ? 11000 : 4300;
    const estimated = stages * (labour + cement * s.prices.cement * (1 + freight(s)));
    const reward = round(estimated * (major ? 1.22 : 1.20) / 100) * 100;
    return { id: `${s.turn}-${index}`, type, major, stages, cement, labour, reward, bond: round(reward * .1), requirement: major ? 35 : 5, progress: 0, deadline: s.turn + stages + 1 };
  }
  function makeSeason(s, previousStorm = false) {
    const season = s.turn % 4;
    const stormChance = [.10, .30, .18, .04][season];
    const harvest = random(s);
    const mood = harvest < .20 ? 'Poor harvest reports are lifting rice prices.' : harvest > .80 ? 'A plentiful harvest is softening rice prices.' : 'Staple supplies are steady along the coast.';
    s.weather = { chance: stormChance, label: ['Changeable', 'Storm season', 'Unsettled', 'Fair passage'][season] };
    const shocks = { rice: harvest < .20 ? .16 : harvest > .80 ? -.14 : 0, tea: random(s) < .25 ? .13 : 0, cement: s.turn % 8 < 3 ? .10 : -.04, opium: s.turn >= 24 ? -.03 : .02 };
    if (previousStorm) { shocks.rice += .08; shocks.cement += .08; }
    for (const [k, g] of Object.entries(GOODS)) {
      const seasonal = k === 'rice' ? [.02, .06, -.06, 0][season] : k === 'tea' ? [-.03, .01, .04, 0][season] : 0;
      s.prices[k] = round(clamp(s.prices[k] * .57 + g.base * (1 + s.turn * .003) * (.43 + seasonal + shocks[k] + (random(s) - .5) * .14), g.base * .6, g.base * 2.1));
      s.history[k].push(s.prices[k]);
      s.history[k] = s.history[k].slice(-12);
    }
    s.news = `${mood} ${shocks.tea ? 'Overseas buyers seek more tea. ' : ''}${shocks.cement > 0 ? 'Public building demand is firm.' : 'Construction orders are quieter.'}`;
    if (previousStorm) s.news += ' Storm disruption is putting upward pressure on rice and reconstruction materials.';
    if (s.turn === 16) s.news += ' Regional conflict is disrupting routes; merchants are reassessing their exposure.';
    if (s.turn === 24) s.news += ' Treaty-era changes alter the opium trade. Route enforcement risk eases, but theft and community harm remain.';
    s.sold = emptyGoods();
    const types = Object.keys(PROJECTS);
    s.tenders = [0, 1, 2].map(i => makeTender(s, types[(Math.floor(s.turn / 2) + i * 2) % types.length], s.turn >= 12 && i === 2, i)).filter(c => c.stages <= 72 - s.turn);
    s.event = s.turn > 0 && s.turn % 4 === 1 ? { kind: 'relief', resolved: false } : s.turn > 0 && s.turn % 4 === 3 ? { kind: 'workers', resolved: false } : null;
  }
  function newGame(seed = 'Victoria-1852', name = 'Victoria Trading Company') {
    const s = {
      version: VERSION, seed: String(seed).slice(0, 64), rng: seedNumber(seed), name: String(name).trim().slice(0, 60) || 'Victoria Trading Company',
      turn: 0, cash: 100000, debt: 0, official: 5, trust: 5, stock: emptyGoods(), incoming: [], sold: emptyGoods(),
      prices: Object.fromEntries(Object.entries(GOODS).map(([k, g]) => [k, g.base])), history: Object.fromEntries(Object.keys(GOODS).map(k => [k, []])),
      plots: [], nextPlot: 1, contracts: [], tenders: [], completed: 0, majorCompleted: 0,
      city: { handling: 0, cartage: 0, flood: 0, labour: 0, demand: 0 }, manager: false, insurance: true,
      lastOpium: -8, qualifying: 0, ending: null, distress: false, report: null, log: [], event: null,
      stats: { traded: 0, losses: 0, bestWorth: 100000, relief: 0 }
    };
    makeSeason(s);
    record(s, 'You arrive in Victoria Harbour with $100,000 and the ambition to establish a trading house.');
    return s;
  }
  function requireCondition(condition, message) { if (!condition) throw new Error(message); }
  function pay(s, amount) { requireCondition(s.cash >= amount, 'There is not enough available cash.'); s.cash -= amount; }
  function integer(n) { requireCondition(Number.isSafeInteger(n) && n > 0 && n <= 1000000, 'Enter a positive whole number.'); return n; }
  function opiumTrade(s, qty) {
    s.lastOpium = s.turn;
    standing(s, 0, -Math.min(5, qty * .12));
    s.qualifying = 0;
  }
  function settle(s) {
    s.cash = round(s.cash);
    s.distress = s.cash < 0;
    s.official = Math.round(s.official * 10) / 10;
    s.trust = Math.round(s.trust * 10) / 10;
    s.stats.bestWorth = Math.max(s.stats.bestWorth, netWorth(s));
    if (s.distress) s.qualifying = 0;
    if (s.turn >= 72 && !s.distress && !s.ending) s.ending = 'survived';
  }
  function advance(s) {
    requireCondition(!s.distress, 'Settle the overdue balance before advancing, or declare bankruptcy.');
    const startCash = s.cash;
    const report = { season: date(s), entries: [], expense: operating(s), storm: false, cashChange: 0 };
    const note = text => { report.entries.push(text); record(s, text); };
    s.cash -= report.expense;
    const storm = random(s) < s.weather.chance;
    report.storm = storm;
    note(storm ? 'A coastal storm batters the shipping lanes.' : 'The harbour remains open; shipping conditions are manageable.');
    // Paid construction completes before arrival so opening cargo has a warehouse.
    for (const p of s.plots) if (p.building) { p.building = false; p.built = true; note(`Your warehouse in ${LOCATIONS[p.location].name} opens with 180 storage spaces.`); }
    const stores = s.plots.filter(p => p.built);
    const exposure = stores.length ? stores.reduce((n, p) => n + LOCATIONS[p.location].exposure, 0) / stores.length : 1;
    for (const [k, g] of Object.entries(GOODS)) {
      let rate = g.spoil * (1 - .65 * protection(s, 'ventilation'));
      if (storm) rate += (k === 'cement' ? .16 * (1 - .8 * protection(s, 'dry')) : .045) * exposure * (1 - .6 * protection(s, 'floors')) * (1 - reduction(s, 'flood'));
      const loss = Math.min(s.stock[k], Math.floor(s.stock[k] * rate + random(s)));
      if (loss) { s.stock[k] -= loss; s.stats.losses += round(loss * s.prices[k]); note(`${loss} units of stored ${g.name.toLowerCase()} are lost to ${storm ? 'weather and deterioration' : 'deterioration'}.`); }
    }
    // One route roll per commodity, not per order: splitting cargo cannot evade risk.
    const opiumHit = random(s) < (s.turn < 24 ? .16 : .09) * (1 - .35 * protection(s, 'security'));
    for (const c of s.incoming) {
      let loss = storm ? Math.ceil(c.qty * (.06 + random(s) * .12)) : 0;
      if (c.good === 'opium' && opiumHit) {
        loss = Math.min(c.qty, loss + Math.ceil(c.qty * .65));
        standing(s, -2, -2);
        note('An opium consignment suffers a route seizure or theft. This loss is excluded from insurance.');
      }
      loss = Math.min(c.qty, loss);
      s.stock[c.good] += c.qty - loss;
      if (loss) {
        const value = round(c.value * loss / c.qty);
        const compensation = c.insured && !(c.good === 'opium' && opiumHit) ? round(value * .8) : 0;
        s.cash += compensation;
        s.stats.losses += value - compensation;
        note(`${GOODS[c.good].name}: ${c.qty - loss}/${c.qty} units arrive.${compensation ? ` Insurance pays $${compensation.toLocaleString('en-US')}.` : ''}`);
      } else note(`${GOODS[c.good].name}: ${c.qty} units arrive safely.`);
    }
    s.incoming = [];
    for (const c of [...s.contracts]) {
      const cost = contractCost(s, c);
      if (storm && random(s) < .22) note(`${PROJECTS[c.type].name}: weather delays this season’s work.`);
      else if (s.cash < round(cost.cash)) note(`${PROJECTS[c.type].name}: work pauses because working capital is insufficient.`);
      else {
        s.cash -= round(cost.cash);
        s.stock.cement -= cost.cement;
        c.progress++;
        const payment = c.progress === c.stages ? c.reward - Math.floor(c.reward * .20) * (c.stages - 1) : Math.floor(c.reward * .20);
        s.cash += payment;
        note(`${PROJECTS[c.type].name}: stage ${c.progress}/${c.stages} delivered; payment $${payment.toLocaleString('en-US')}.`);
        if (c.progress === c.stages) {
          s.cash += c.bond;
          s.completed++;
          if (c.major) s.majorCompleted++;
          s.city[PROJECTS[c.type].effect]++;
          standing(s, c.major ? 16 : 10, c.major ? 12 : 8);
          s.contracts = s.contracts.filter(item => item.id !== c.id);
          note(`${PROJECTS[c.type].name} completed. Your bond is returned and the city benefits.`);
          continue;
        }
      }
      if (s.turn >= c.deadline || s.turn === 71) {
        s.contracts = s.contracts.filter(item => item.id !== c.id);
        s.cash -= round(c.reward * .05);
        standing(s, -15, -8);
        s.qualifying = 0;
        note(`${PROJECTS[c.type].name} defaults${s.turn === 71 ? ' at the final settlement' : ''}: bond forfeited and a 5% penalty is payable.`);
      }
    }
    if (s.stock.opium > 0) { s.lastOpium = s.turn; standing(s, 0, -.5); }
    if (s.cash >= 0 && s.plots.some(p => p.built)) {
      // Routine reliability has a ceiling; high standing requires actual achievements.
      if (s.official < 25) s.official = Math.min(25, s.official + .5);
      if (s.trust < 20 && s.turn - s.lastOpium > 0) s.trust = Math.min(20, s.trust + .35);
    }
    s.qualifying = eligible(s) ? s.qualifying + 1 : 0;
    s.turn++;
    if (s.turn % 4 === 0 && s.qualifying >= 4 && s.cash >= 0) s.ending = 'governor';
    if (s.turn > 0 && s.turn % 12 === 0 && s.turn < 72) {
      const keys = Object.keys(s.city);
      const effect = keys[Math.floor(random(s) * keys.length)];
      s.city[effect]++;
      note(`Another merchant finishes a public project. The city’s ${effect} infrastructure improves.`);
    }
    if (s.turn < 72 && !s.ending) makeSeason(s, storm);
    report.cashChange = round(s.cash - startCash);
    s.report = report;
    settle(s);
    if (s.distress) record(s, 'Payments exceed your cash. Liquidate stock or property, or arrange credit before continuing.', 'bad');
    if (s.ending) record(s, s.ending === 'governor' ? 'A dispatch from London confirms your appointment as Governor of Hong Kong.' : '1870 dawns. Your trading house has endured.', 'good');
  }
  function act(state, action) {
    const s = clone(state);
    requireCondition(action && typeof action.type === 'string', 'Invalid action.');
    requireCondition(!s.ending, 'This campaign has ended. Start a new house to play again.');
    if (s.distress) requireCondition(['sell', 'borrow', 'liquidate', 'abandon', 'bankrupt'].includes(action.type), 'Settle your overdue balance first.');
    switch (action.type) {
      case 'establish': {
        requireCondition(s.plots.length === 0, 'Your house is already established.');
        pay(s, 35000);
        s.plots.push({ id: s.nextPlot++, location: 'town', price: 20000, built: false, building: true, upgrades: [] });
        record(s, 'You secure a Victoria town lease and commission your first warehouse. It will open next season.', 'good');
        break;
      }
      case 'buy': {
        requireCondition(Object.hasOwn(GOODS, action.good), 'Unknown commodity.');
        const qty = integer(action.qty);
        requireCondition(usedSpace(s) + qty * GOODS[action.good].space <= capacity(s, true), 'There is not enough warehouse space, including incoming cargo.');
        const cost = buyQuote(s, action.good, qty);
        pay(s, cost);
        const existing = s.incoming.find(c => c.good === action.good && c.insured === s.insurance);
        if (existing) { existing.qty += qty; existing.value += s.prices[action.good] * qty; }
        else s.incoming.push({ good: action.good, qty, value: s.prices[action.good] * qty, insured: s.insurance });
        if (action.good === 'opium') opiumTrade(s, qty);
        s.stats.traded += cost;
        record(s, `Ordered ${qty} ${GOODS[action.good].name.toLowerCase()} for $${cost.toLocaleString('en-US')}; arrival next season.`);
        break;
      }
      case 'sell': {
        requireCondition(Object.hasOwn(GOODS, action.good), 'Unknown commodity.');
        const qty = integer(action.qty);
        requireCondition(s.stock[action.good] >= qty, 'You do not hold that much saleable stock.');
        const amount = sellQuote(s, action.good, qty);
        s.stock[action.good] -= qty;
        s.sold[action.good] += qty;
        s.cash += amount;
        if (action.good === 'opium') opiumTrade(s, qty);
        s.stats.traded += amount;
        record(s, `Sold ${qty} ${GOODS[action.good].name.toLowerCase()} for $${amount.toLocaleString('en-US')}.`);
        break;
      }
      case 'land': {
        requireCondition(Object.hasOwn(LOCATIONS, action.location), 'Unknown location.');
        requireCondition(s.plots.length < 6, 'The house can hold at most six plots.');
        const price = round(LOCATIONS[action.location].price * (1 + s.turn * .007));
        pay(s, price);
        s.plots.push({ id: s.nextPlot++, location: action.location, price, built: false, building: false, upgrades: [] });
        record(s, `Purchased a lease in ${LOCATIONS[action.location].name}.`);
        break;
      }
      case 'build': {
        const p = s.plots.find(p => p.id === action.id);
        requireCondition(p && !p.built && !p.building, 'Select an empty plot.');
        requireCondition(activeProjects(s) < (s.manager ? 2 : 1), 'All project supervision slots are occupied.');
        pay(s, 15000); p.building = true;
        record(s, 'Warehouse commissioned. It opens next season.'); break;
      }
      case 'upgrade': {
        const p = s.plots.find(p => p.id === action.id);
        requireCondition(p && p.built && Object.hasOwn(UPGRADES, action.upgrade), 'Select a built warehouse and a valid improvement.');
        requireCondition(!p.upgrades.includes(action.upgrade), 'That improvement is already installed.');
        pay(s, UPGRADES[action.upgrade].price); p.upgrades.push(action.upgrade);
        record(s, `${UPGRADES[action.upgrade].name} installed in warehouse ${p.id}.`); break;
      }
      case 'liquidate': {
        const p = s.plots.find(p => p.id === action.id);
        requireCondition(p, 'Plot not found.');
        const remaining = clone(s); remaining.plots = remaining.plots.filter(item => item.id !== p.id);
        requireCondition(usedSpace(s) <= capacity(remaining, true), 'Sell enough stock first; remaining warehouses must hold all cargo.');
        const amount = round((p.price + (p.built ? 15000 : p.building ? 10000 : 0) + p.upgrades.reduce((n, u) => n + UPGRADES[u].price, 0)) * .65);
        s.plots = remaining.plots; s.cash += amount;
        record(s, `Property ${p.id} liquidated for $${amount.toLocaleString('en-US')} (65% of book value).`); break;
      }
      case 'contract': {
        const c = s.tenders.find(c => c.id === action.id);
        requireCondition(c && !s.contracts.some(item => item.id === c.id), 'This tender is no longer available.');
        requireCondition(s.plots.some(p => p.built), 'Open a warehouse before tendering for public work.');
        requireCondition(s.official >= c.requirement, `This tender requires ${c.requirement} Official Standing.`);
        requireCondition(activeProjects(s) < (s.manager ? 2 : 1), 'All project supervision slots are occupied.');
        pay(s, c.bond); s.contracts.push(clone(c)); s.tenders = s.tenders.filter(item => item.id !== c.id);
        record(s, `${PROJECTS[c.type].name} awarded. Performance bond posted.`); break;
      }
      case 'abandon': {
        const c = s.contracts.find(c => c.id === action.id);
        requireCondition(c, 'Contract not found.');
        s.contracts = s.contracts.filter(item => item.id !== c.id);
        s.cash -= round(c.reward * .05); standing(s, -15, -8); s.qualifying = 0;
        record(s, 'Contract abandoned. Your bond is forfeited and a 5% penalty is payable.', 'bad'); break;
      }
      case 'borrow': {
        const amount = integer(action.amount);
        requireCondition(s.debt + amount <= creditLimit(s), 'This loan exceeds your secured credit limit.');
        s.cash += amount; s.debt += amount; record(s, `Borrowed $${amount.toLocaleString('en-US')} at 2.5% seasonal interest.`); break;
      }
      case 'repay': {
        const amount = integer(action.amount); requireCondition(amount <= s.debt, 'That exceeds the outstanding debt.');
        pay(s, amount); s.debt -= amount; record(s, `Repaid $${amount.toLocaleString('en-US')} of principal.`); break;
      }
      case 'insurance': s.insurance = Boolean(action.enabled); break;
      case 'manager':
        requireCondition(!s.manager, 'A superintendent is already employed.');
        pay(s, 3000); s.manager = true; record(s, 'Superintendent hired: two project slots, $650 additional seasonal salary.'); break;
      case 'event': {
        requireCondition(s.event && !s.event.resolved, 'There is no outstanding seasonal decision.');
        requireCondition(['help', 'decline'].includes(action.choice), 'Choose a valid response.');
        if (action.choice === 'help' && s.event.kind === 'relief') {
          requireCondition(s.stock.rice >= 20, 'The relief committee needs 20 units of rice already in store.');
          s.stock.rice -= 20; s.cash += round(20 * s.prices.rice * 1.03);
          const gain = Math.max(1, 6 - s.stats.relief * .5); s.stats.relief++;
          standing(s, 2, gain); record(s, 'You supply the relief committee at a restrained price. Residents remember your assistance.', 'good');
        } else if (action.choice === 'help') {
          pay(s, 1800); standing(s, 1, s.trust < 50 ? 3 : 1);
          record(s, 'You fund a workers’ clinic and paid recovery time.', 'good');
        } else record(s, 'You decline the seasonal appeal and preserve working capital.');
        s.event.resolved = true; break;
      }
      case 'end': advance(s); break;
      case 'bankrupt':
        requireCondition(s.distress, 'Bankruptcy is available only when an obligation is overdue.');
        s.ending = 'bankrupt'; record(s, 'Unable to settle its obligations, the house enters bankruptcy.', 'bad'); break;
      default: throw new Error('Unknown action.');
    }
    settle(s);
    return s;
  }
  // Saves are untrusted input. Validate nested structures before any rendering or simulation.
  function validateSave(input) {
    requireCondition(input && typeof input === 'object' && input.version === VERSION, 'Unsupported save version.');
    const s = clone(input);
    const num = (v, lo, hi, whole = false) => typeof v === 'number' && Number.isFinite(v) && v >= lo && v <= hi && (!whole || Number.isInteger(v));
    const text = (v, max) => typeof v === 'string' && v.length <= max;
    const bool = v => typeof v === 'boolean';
    const check = (v, message = 'Invalid or damaged save file.') => requireCondition(v, message);
    check(text(s.name, 60) && text(s.seed, 64) && num(s.rng, 0, 4294967295, true));
    check(num(s.turn, 0, 72, true) && num(s.cash, -1e9, 1e12, true) && num(s.debt, 0, 1e12, true));
    for (const k of ['official', 'trust']) check(num(s[k], 0, 100));
    for (const k of ['completed', 'majorCompleted', 'qualifying']) check(num(s[k], 0, 200, true));
    check(s.majorCompleted <= s.completed && num(s.lastOpium, -8, s.turn, true) && num(s.nextPlot, 1, 1000, true));
    check(bool(s.manager) && bool(s.insurance) && bool(s.distress) && [null, 'governor', 'survived', 'bankrupt'].includes(s.ending));
    check(s.distress === (s.cash < 0));
    for (const key of ['stock', 'sold', 'prices', 'history']) check(s[key] && typeof s[key] === 'object');
    for (const k of Object.keys(GOODS)) {
      check(num(s.stock[k], 0, 1000000, true) && num(s.sold[k], 0, 1000000, true) && num(s.prices[k], 1, 1000000, true));
      check(Array.isArray(s.history[k]) && s.history[k].length <= 12 && s.history[k].every(v => num(v, 1, 1000000, true)));
    }
    check(Array.isArray(s.incoming) && s.incoming.length <= 8);
    check(s.incoming.every(c => c && Object.hasOwn(GOODS, c.good) && num(c.qty, 1, 1000000, true) && num(c.value, 1, 1e12) && bool(c.insured)));
    check(Array.isArray(s.plots) && s.plots.length <= 6);
    for (const p of s.plots) check(p && num(p.id, 1, s.nextPlot - 1, true) && Object.hasOwn(LOCATIONS, p.location) && num(p.price, 1, 1e9) && bool(p.built) && bool(p.building) && !(p.built && p.building) && Array.isArray(p.upgrades) && p.upgrades.length <= 5 && p.upgrades.every(u => Object.hasOwn(UPGRADES, u)) && new Set(p.upgrades).size === p.upgrades.length);
    check(new Set(s.plots.map(p => p.id)).size === s.plots.length);
    const validContract = c => c && text(c.id, 30) && Object.hasOwn(PROJECTS, c.type) && bool(c.major) && num(c.stages, 3, 4, true) && num(c.progress, 0, c.stages - 1, true) && num(c.cement, 1, 1000, true) && num(c.labour, 1, 1e7, true) && num(c.reward, 1, 1e9, true) && num(c.bond, 0, 1e9, true) && num(c.requirement, 0, 100) && num(c.deadline, 0, 80, true);
    check(Array.isArray(s.contracts) && s.contracts.length <= 2 && s.contracts.every(validContract));
    check(Array.isArray(s.tenders) && s.tenders.length <= 3 && s.tenders.every(validContract));
    check(new Set([...s.contracts, ...s.tenders].map(c => c.id)).size === s.contracts.length + s.tenders.length);
    check(s.city && Object.keys(PROJECTS).every(k => num(s.city[PROJECTS[k].effect], 0, 200, true)));
    check(s.weather && num(s.weather.chance, 0, 1) && text(s.weather.label, 80) && text(s.news, 2000));
    check(s.event === null || (s.event && ['relief', 'workers'].includes(s.event.kind) && bool(s.event.resolved)));
    check(s.stats && ['traded', 'losses', 'bestWorth', 'relief'].every(k => num(s.stats[k], 0, 1e15)));
    check(Array.isArray(s.log) && s.log.length <= 160 && s.log.every(l => l && num(l.turn, 0, 72, true) && text(l.text, 2000) && ['neutral', 'good', 'bad'].includes(l.tone)));
    check(s.report === null || (s.report && text(s.report.season, 80) && Array.isArray(s.report.entries) && s.report.entries.length <= 100 && s.report.entries.every(e => text(e, 2000)) && num(s.report.expense, 0, 1e12) && bool(s.report.storm) && num(s.report.cashChange, -1e12, 1e12)));
    check(usedSpace(s) <= capacity(s, true) && activeProjects(s) <= (s.manager ? 2 : 1));
    check(s.turn < 72 || Boolean(s.ending) || s.distress);
    return s;
  }
  function serialize(s) { return JSON.stringify(validateSave(s), null, 2); }
  function deserialize(text) {
    requireCondition(typeof text === 'string' && text.length <= 1000000, 'Save file is too large.');
    try { return validateSave(JSON.parse(text)); } catch (error) { throw new Error(`Cannot load save: ${error.message}`); }
  }
  return { VERSION, GOODS, LOCATIONS, PROJECTS, UPGRADES, SEASONS, newGame, act, date, capacity, usedSpace, operating, commitments, propertyValue, netWorth, creditLimit, buyQuote, sellQuote, demand, contractCost, activeProjects, appointment, reduction, serialize, deserialize, validateSave };
});
