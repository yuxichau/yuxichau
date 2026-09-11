const { test } = require('node:test');
const assert = require('node:assert/strict');
const E = require('../engine.js');

function opening(seed = 'test') {
  return E.act(E.newGame(seed), { type: 'establish' });
}
function advance(s, turns = 1) {
  for (let i = 0; i < turns; i++) s = E.act(s, { type: 'end' });
  return s;
}

test('opening costs, warehouse lead time, and cargo settlement', () => {
  let s = opening();
  assert.equal(s.cash, 65000);
  assert.equal(E.capacity(s), 0);
  assert.equal(E.capacity(s, true), 180);
  const before = E.serialize(s);
  s = E.act(s, { type: 'buy', good: 'tea', qty: 50 });
  assert.equal(s.stock.tea, 0);
  assert.equal(s.incoming[0].qty, 50);
  assert.throws(() => E.act(s, { type: 'sell', good: 'tea', qty: 1 }), /saleable/);
  s = advance(s);
  assert.equal(E.capacity(s), 180);
  assert.ok(s.stock.tea > 0);
  assert.equal(s.incoming.length, 0);
  assert.equal(E.deserialize(before).cash, 65000);
  E.validateSave(s);
});

test('failed actions are atomic and reject invalid quantities and keys', () => {
  const s = opening();
  const original = E.serialize(s);
  for (const qty of [-2, 0, .5, NaN, Infinity, 1000001]) assert.throws(() => E.act(s, { type: 'buy', good: 'tea', qty }));
  for (const good of ['gold', '__proto__', 'constructor']) assert.throws(() => E.act(s, { type: 'buy', good, qty: 1 }));
  assert.throws(() => E.act(s, { type: 'buy', good: 'rice', qty: 181 }), /space/);
  assert.equal(E.serialize(s), original);
});

test('seed and save round-trip preserve future simulation exactly', () => {
  let a = opening('same-seed');
  a = E.act(a, { type: 'buy', good: 'rice', qty: 80 });
  const b = E.deserialize(E.serialize(a));
  assert.deepEqual(advance(a, 8), advance(b, 8));
  assert.notDeepEqual(E.newGame('different').prices, a.prices);
});

test('market depth applies across repeated sales within the same season', () => {
  let s = opening();
  s.stock.rice = 180;
  s.sold.rice = E.demand(s, 'rice') - 10;
  const whole = E.sellQuote(s, 'rice', 100);
  const first = E.sellQuote(s, 'rice', 50);
  s = E.act(s, { type: 'sell', good: 'rice', qty: 50 });
  const second = E.sellQuote(s, 'rice', 50);
  assert.ok(Math.abs(whole - first - second) <= 1);
  assert.ok(second < first);
});

test('insurance changes the price and orders consolidate to resist splitting risk', () => {
  let s = opening();
  assert.ok(E.buyQuote(s, 'tea', 10, true) > E.buyQuote(s, 'tea', 10, false));
  s = E.act(s, { type: 'buy', good: 'tea', qty: 10 });
  s = E.act(s, { type: 'buy', good: 'tea', qty: 10 });
  assert.equal(s.incoming.length, 1);
  assert.equal(s.incoming[0].qty, 20);
});

test('public work requires supervision, pays milestones, returns bond, and improves city', () => {
  let s = advance(opening('contract'));
  const tender = s.tenders[0];
  s = E.act(s, { type: 'contract', id: tender.id });
  assert.equal(s.contracts.length, 1);
  assert.throws(() => E.act(s, { type: 'contract', id: s.tenders[0].id }), /slots/);
  for (let i = 0; i < 6 && s.contracts.length; i++) s = advance(s);
  assert.equal(s.completed, 1);
  assert.equal(s.contracts.length, 0);
  assert.ok(s.city[E.PROJECTS[tender.type].effect] >= 1);
  assert.ok(s.official >= 15);
  E.validateSave(s);
});

test('a starved project defaults and cannot mint milestone payments', () => {
  let s = advance(opening('default'));
  s = E.act(s, { type: 'contract', id: s.tenders[0].id });
  const deadline = s.contracts[0].deadline;
  while (s.turn <= deadline) {
    s.cash = E.operating(s) + 1;
    s = advance(s);
  }
  assert.equal(s.completed, 0);
  assert.equal(s.contracts.length, 0);
  assert.equal(s.distress, true);
  assert.ok(s.log.some(l => l.text.includes('defaults')));
});

test('illiquidity allows rescue; bankruptcy is an explicit ending', () => {
  let s = advance(opening());
  s.cash = 0;
  s = advance(s);
  assert.ok(s.distress);
  assert.equal(s.ending, null);
  assert.throws(() => advance(s), /overdue/);
  const rescued = E.act(s, { type: 'borrow', amount: 3000 });
  assert.equal(rescued.distress, false);
  assert.equal(rescued.debt, 3000);
  const bankrupt = E.act(s, { type: 'bankrupt' });
  assert.equal(bankrupt.ending, 'bankrupt');
  assert.throws(() => advance(bankrupt), /ended/);
});

test('property cannot be sold out from under stored or incoming cargo', () => {
  let s = opening();
  s = E.act(s, { type: 'buy', good: 'rice', qty: 20 });
  assert.throws(() => E.act(s, { type: 'liquidate', id: 1 }), /Sell enough/);
  s = advance(s);
  s = E.act(s, { type: 'sell', good: 'rice', qty: s.stock.rice });
  s = E.act(s, { type: 'liquidate', id: 1 });
  assert.equal(s.plots.length, 0);
});

test('reputation cannot be farmed with repeated seasonal decisions', () => {
  let s = advance(opening());
  s.stock.rice = 20;
  s = E.act(s, { type: 'event', choice: 'help' });
  const trust = s.trust;
  assert.throws(() => E.act(s, { type: 'event', choice: 'help' }), /outstanding/);
  assert.equal(s.trust, trust);
});

test('governorship requires four consecutive qualifying seasons and annual review', () => {
  let s = advance(opening());
  s.turn = 32;
  s.cash = 450000;
  s.official = 80;
  s.trust = 70;
  s.completed = 4;
  s.majorCompleted = 2;
  s.lastOpium = 20;
  for (let i = 0; i < 3; i++) {
    s = advance(s);
    assert.equal(s.ending, null);
  }
  s = advance(s);
  assert.equal(s.ending, 'governor');
  assert.equal(s.turn, 36);
});

test('holding opium prevents an appointment even without new purchases', () => {
  let s = advance(opening());
  Object.assign(s, { turn: 35, cash: 500000, official: 90, trust: 90, completed: 5, majorCompleted: 3, qualifying: 3 });
  s.stock.opium = 1;
  s = advance(s);
  assert.equal(s.qualifying, 0);
  assert.equal(s.ending, null);
});

test('campaign ends exactly when 1870 begins, after final obligations', () => {
  let s = E.newGame();
  s = advance(s, 72);
  assert.equal(s.turn, 72);
  assert.equal(E.date(s), 'Spring 1870');
  assert.equal(s.ending, 'survived');
  s = E.newGame();
  s.turn = 71; s.cash = 0;
  s = advance(s);
  assert.equal(s.ending, null);
  assert.ok(s.distress);
  assert.equal(E.act(s, { type: 'bankrupt' }).ending, 'bankrupt');
});

test('damaged saves fail before rendering, including nested structures', () => {
  const original = E.newGame();
  for (const damage of [s => s.version = 2, s => s.history.tea = null, s => s.stock.tea = -2, s => s.log = [{ text: 2 }], s => s.contracts = [{}], s => s.city = {}, s => s.weather.chance = 8, s => s.distress = true]) {
    const s = structuredClone(original); damage(s);
    assert.throws(() => E.deserialize(JSON.stringify(s)));
  }
  assert.throws(() => E.deserialize('{bad json'));
  assert.throws(() => E.deserialize('x'.repeat(1000001)), /large/);
});

test('infrastructure has a hard diminishing-return cap', () => {
  const s = E.newGame();
  s.city.handling = 100;
  assert.equal(E.reduction(s, 'handling'), .28);
});

test('weather disruption affects subsequent commodity prices and market news', () => {
  let storm = opening('weather-link');
  let fair = structuredClone(storm);
  storm.weather.chance = 1;
  fair.weather.chance = 0;
  storm = advance(storm);
  fair = advance(fair);
  assert.ok(storm.prices.rice > fair.prices.rice);
  assert.ok(storm.prices.cement > fair.prices.cement);
  assert.match(storm.news, /Storm disruption/);
});

test('final settlement closes unfinished contracts and avoids impossible late tenders', () => {
  let s = advance(opening('final-project'));
  s = E.act(s, { type: 'contract', id: s.tenders[0].id });
  s.turn = 71;
  s.contracts[0].deadline = 75;
  s.cash = E.operating(s) + 1;
  s = advance(s);
  assert.equal(s.contracts.length, 0);
  assert.equal(s.completed, 0);
  assert.ok(s.distress);
  assert.match(s.log.map(l => l.text).join(' '), /final settlement/);
  s = E.newGame(); s.turn = 69;
  s = advance(s);
  assert.equal(s.tenders.length, 0);
});

test('multi-seed prudent tea/rice strategy remains playable for full campaigns', () => {
  const outcomes = [];
  for (let seed = 0; seed < 30; seed++) {
    let s = opening(`campaign-${seed}`);
    while (!s.ending && !s.distress) {
      for (const good of ['tea', 'rice']) if (s.stock[good]) s = E.act(s, { type: 'sell', good, qty: s.stock[good] });
      if (s.cash > 35000) {
        const qty = Math.min(80, Math.floor((s.cash - 18000) / E.buyQuote(s, 'tea', 1)), E.capacity(s, true) - E.usedSpace(s));
        if (qty > 0) s = E.act(s, { type: 'buy', good: 'tea', qty });
      }
      s = advance(s);
      E.validateSave(s);
    }
    outcomes.push({ ending: s.ending, worth: E.netWorth(s) });
  }
  assert.ok(outcomes.filter(o => o.ending === 'survived').length >= 27, JSON.stringify(outcomes));
  assert.ok(outcomes.filter(o => o.worth > 100000).length >= 24, JSON.stringify(outcomes));
});
