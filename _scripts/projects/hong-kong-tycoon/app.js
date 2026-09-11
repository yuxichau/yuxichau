(function () {
  'use strict';
  const E = window.Tycoon;
  const SAVE_KEY = 'hong-kong-tycoon-save-v1';
  const $ = selector => document.querySelector(selector);
  const esc = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const money = n => `${n < 0 ? '−' : ''}$${Math.abs(Math.round(n)).toLocaleString('en-US')}`;
  const signed = n => `${n >= 0 ? '+' : '−'}$${Math.abs(Math.round(n)).toLocaleString('en-US')}`;
  const disabled = condition => condition ? ' disabled' : '';
  let state = E.newGame();
  let tab = 'exchange';
  let storageMessage = 'Progress is saved on this device.';
  let toastTimer;
  let recovered = false;
  let saveBlocked = false;
  const quantities = { rice: 20, tea: 20, cement: 20, opium: 5 };
  let confirmAction = null;
  let focusBeforeModal = null;

  try {
    const saved = localStorage.getItem(SAVE_KEY);
    if (saved) { state = E.deserialize(saved); recovered = true; }
  } catch (error) {
    storageMessage = 'Save unavailable. Export your game to keep it.';
    saveBlocked = true;
    // Do not overwrite a damaged existing save until the player explicitly starts/imports.
  }

  function save() {
    if (saveBlocked) return;
    try { localStorage.setItem(SAVE_KEY, E.serialize(state)); storageMessage = 'Autosaved · stored on this device'; }
    catch { storageMessage = 'Autosave unavailable · use Export save'; }
  }
  function toast(message) {
    clearTimeout(toastTimer);
    $('#toast').textContent = message;
    $('#toast').classList.add('visible');
    toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 4200);
  }
  function modal(title, body, actions = '') {
    const dialog = $('#modal');
    if (!dialog.open) focusBeforeModal = document.activeElement;
    $('#modal-body').innerHTML = `<div class="modal-header"><h2 id="modal-title">${esc(title)}</h2><button type="button" data-ui="close" aria-label="Close dialog">×</button></div>${body}${actions ? `<div class="modal-actions">${actions}</div>` : ''}`;
    if (!dialog.open) dialog.showModal();
  }
  function closeModal() {
    $('#modal').close();
    confirmAction = null;
    if (focusBeforeModal?.isConnected) focusBeforeModal.focus();
  }
  function confirm(title, body, action, label = 'Confirm') {
    confirmAction = action;
    modal(title, body, `<button type="button" data-ui="close">Cancel</button><button type="button" class="primary" data-ui="confirm">${esc(label)}</button>`);
  }
  function dispatch(action, message) {
    try {
      state = E.act(state, action);
      save(); render();
      if (message) toast(message);
      if (action.type === 'end') showReport();
      return true;
    } catch (error) { toast(error.message); return false; }
  }
  function progress(value, max, label) { return `<progress class="meter" max="${max}" value="${Math.max(0, Math.min(max, value))}" aria-label="${esc(label)}"></progress>`; }
  function ledgerRow(label, value, cls = '') { return `<div class="ledger-row"><span>${label}</span><strong class="${cls}">${value}</strong></div>`; }
  function renderLedger() {
    const obligations = E.commitments(state);
    const reserve = state.cash - obligations;
    const pending = state.incoming.reduce((n, c) => n + c.qty, 0);
    $('#ledger').innerHTML = `
      <div class="ledger-section"><p class="eyebrow">The house ledger</p><div class="season">${E.date(state)}</div><span class="small muted">${state.turn >= 72 ? 'The campaign is complete' : `Season ${state.turn + 1} of 72`}</span><div class="campaign-progress" aria-hidden="true">${Array.from({ length: 18 }, (_, i) => `<span class="${i < Math.ceil(state.turn / 4) ? 'filled' : ''}"></span>`).join('')}</div><p class="eyebrow">Available cash</p><div class="cash-value money ${state.cash < 0 ? 'negative' : ''}">${money(state.cash)}</div></div>
      <div class="ledger-section">${ledgerRow('Net worth', money(E.netWorth(state)))}${ledgerRow('Debt', money(state.debt))}${ledgerRow('Seasonal expenses', money(E.operating(state)))}${ledgerRow('Works cash needed', money(obligations - E.operating(state)))}<div class="reserve ${reserve < 0 ? 'warning' : ''}"><p>After upcoming commitments</p><strong class="money ${reserve < 0 ? 'negative' : 'positive'}">${money(reserve)}</strong></div><button type="button" class="text-button small" data-ui="bank">Arrange credit →</button></div>
      <div class="ledger-section">${ledgerRow('Official Standing', `${state.official.toFixed(1)} / 100`)}${progress(state.official, 100, 'Official Standing')}${ledgerRow('Public Trust', `${state.trust.toFixed(1)} / 100`)}${progress(state.trust, 100, 'Public Trust')}</div>
      <div class="ledger-section">${ledgerRow('Warehouse space', `${E.usedSpace(state)} / ${E.capacity(state, true)}`)}${progress(E.usedSpace(state), Math.max(1, E.capacity(state, true)), 'Warehouse space in use')}${ledgerRow('Incoming cargo', `${pending} units`)}${ledgerRow('Project supervision', `${E.activeProjects(state)} / ${state.manager ? 2 : 1}`)}</div>`;
    const end = $('[data-ui="end"]');
    end.disabled = Boolean(state.ending || state.distress);
    end.innerHTML = state.ending ? 'Campaign concluded' : state.distress ? 'Settle overdue balance' : 'Close the season <span aria-hidden="true">→</span>';
    $('#save-status').textContent = storageMessage;
    $('#house-name').textContent = state.name;
  }
  function endingMarkup() {
    const title = state.ending === 'governor' ? 'His Excellency, the Governor' : state.ending === 'bankrupt' ? 'The House Falls Silent' : 'The House Endures';
    const legacy = state.trust >= 60 ? 'a respected civic merchant' : state.turn - state.lastOpium < 8 ? 'a prosperous but contested opium trader' : E.propertyValue(state) >= 150000 ? 'a harbour property baron' : E.netWorth(state) >= 250000 ? 'an established merchant of Victoria' : 'a determined survivor';
    const story = state.ending === 'governor' ? `A dispatch from London confirms your appointment. Through commerce, public works, and sustained public confidence, ${esc(state.name)} has changed the harbour. You leave the counting house for Government House.` : state.ending === 'bankrupt' ? `The creditors gather, the warehouse doors close, and the final ledger of ${esc(state.name)} is signed. Your ambition outpaced your working capital.` : `As 1870 dawns, ${esc(state.name)} is still trading. You are remembered as ${legacy}. The harbour you first entered eighteen years ago is a different place.`;
    return `<section class="ending"><p class="eyebrow">${state.ending === 'governor' ? 'The appointment' : 'Your final chapter'}</p><h2>${title}</h2><p>${story}</p><p class="small muted">Final net worth ${money(E.netWorth(state))} · ${state.completed} public contracts · Public Trust ${state.trust.toFixed(1)}</p><div class="actions"><button type="button" data-ui="new" class="primary">Establish another house</button><button type="button" data-ui="export">Keep this chronicle</button></div></section>`;
  }
  function renderAlerts() {
    $('#alerts').innerHTML = state.ending ? endingMarkup() : state.distress ? `<section class="notice warning"><p class="eyebrow">Creditors at the door</p><h3>${money(-state.cash)} is overdue</h3><p>Your house still has time to raise the money. Sell stored cargo, arrange secured credit, or liquidate a property on the Estate page.</p><div class="actions"><button type="button" data-ui="bank">Visit the bank</button><button type="button" data-ui="bankrupt" class="danger">Declare bankruptcy</button></div></section>` : '';
  }
  function renderBulletin() {
    $('#bulletin').innerHTML = `<div><p class="eyebrow">The Harbour Gazette</p><h2>Intelligence from the waterfront</h2><p>${esc(state.news)}</p></div><div class="weather"><span class="eyebrow">${state.ending ? 'Last outlook' : 'This season'}</span><strong>${esc(state.weather.label)}</strong><small>${Math.round(state.weather.chance * 100)}% storm risk</small></div>`;
  }
  function spark(good) {
    const values = state.history[good];
    const lo = Math.min(...values) * .95, hi = Math.max(...values) * 1.05;
    const points = (values.length === 1 ? [values[0], values[0]] : values).map((v, i, all) => `${i / (all.length - 1) * 260},${32 - (v - lo) / (hi - lo) * 27}`).join(' ');
    return `<svg class="spark" viewBox="0 0 260 37" preserveAspectRatio="none" role="img" aria-label="${esc(E.GOODS[good].name)} supplier prices over ${values.length} seasons"><title>${values.map(money).join(', ')}</title><line x1="0" y1="35" x2="260" y2="35"></line><polyline points="${points}"></polyline></svg>`;
  }
  function eventMarkup() {
    if (!state.event || state.event.resolved || state.ending) return '';
    const relief = state.event.kind === 'relief';
    return `<section class="card event"><p class="eyebrow">A seasonal decision</p><h3>${relief ? 'An appeal from the relief committee' : 'The men behind the ledgers'}</h3><p>${relief ? 'Local families face an uncertain food supply. The committee asks for 20 units of rice at 3% above today’s supplier price. A smaller margin can earn lasting goodwill.' : 'Dockworkers request a clinic fund and paid recovery time. Contribute $1,800 to support their families and improve public confidence in your house.'}</p><div class="actions"><button type="button" data-action="event" data-choice="help"${disabled(state.distress || (relief ? state.stock.rice < 20 : state.cash < 1800))}>${relief ? `Supply 20 rice · receive ${money(state.prices.rice * 20 * 1.03)}` : 'Contribute $1,800'}</button><button type="button" data-action="event" data-choice="decline"${disabled(state.distress)}>Preserve working capital</button></div></section>`;
  }
  function exchange() {
    const opening = state.plots.length === 0 && state.turn === 0 ? `<section class="notice"><p class="eyebrow">Your first foothold</p><h3>A place on the harbour</h3><p>Secure a Victoria town lease and commission a warehouse for <strong>$35,000</strong>. Your 180-space store opens next season, in time for cargo you order today.</p><div class="actions"><button type="button" data-action="establish" class="primary">Establish the house · $35,000</button><button type="button" data-tab="estate">Choose my own location</button></div></section>` : '';
    return `${opening}<div class="section-heading"><div><p class="eyebrow">The trading exchange</p><h2>Cargo & opportunity</h2><p>Order today. Receive next season. Sell what is already in store.</p></div><label class="check-label"><input type="checkbox" id="insurance"${state.insurance ? ' checked' : ''}${disabled(state.ending || state.distress)}>Insure new cargo · 3%</label></div><div class="commodity-grid">${Object.entries(E.GOODS).map(([k, g]) => {
      const incoming = state.incoming.filter(c => c.good === k).reduce((n, c) => n + c.qty, 0);
      const depth = Math.max(0, E.demand(state, k) - state.sold[k]);
      return `<article class="commodity"><div class="commodity-header"><div><h3>${g.name}</h3><span class="small muted">${g.space} space${g.space === 1 ? '' : 's'} per unit</span></div><span class="badge ${k === 'opium' ? 'risk' : ''}">${{ rice: 'Staple', tea: 'Export', cement: 'Building', opium: 'High risk' }[k]}</span></div><p class="description">${g.description}</p>${spark(k)}<div class="price-row"><div><span>Buy · all-in / unit</span><strong>${money(E.buyQuote(state, k, 1))}</strong></div><div><span>Sell / unit${depth ? '' : ' · excess'}</span><strong>${money(E.sellQuote(state, k, 1))}</strong></div></div><div class="stock-row"><span>In store <strong>${state.stock[k]}</strong></span><span>At sea <strong>${incoming}</strong></span><span>Buyers <strong>${depth}</strong></span></div><div class="trade-input"><label for="qty-${k}">Units</label><input id="qty-${k}" data-qty="${k}" type="number" inputmode="numeric" min="1" max="1000000" step="1" value="${quantities[k]}"><button type="button" data-ui="max-buy" data-good="${k}" title="Fill available space while reserving upcoming commitments">Budget max</button><button type="button" data-ui="all" data-good="${k}">All held</button></div><div class="trade-buttons"><button type="button" class="primary" data-trade="buy" data-good="${k}"${disabled(state.ending || state.distress)}>Order cargo</button><button type="button" data-trade="sell" data-good="${k}"${disabled(state.ending || !state.stock[k])}>Sell stock</button></div><p class="quote" id="quote-${k}"></p></article>`;
    }).join('')}</div><p class="note">Buy prices include freight and selected insurance. Quotes stay fixed throughout the season. Sales beyond remaining market depth earn 22% less. Charts show recent supplier prices. Insurance covers 80% of insured cargo’s purchase value lost to weather; opium route losses are excluded.</p>${eventMarkup()}`;
  }
  function estate() {
    return `<div class="section-heading"><div><p class="eyebrow">Land & stores</p><h2>A foothold in Victoria</h2><p>Land is a long lease. Each warehouse takes one season and a supervision slot to build.</p></div><span class="badge">${state.plots.length} / 6 plots</span></div><div class="cards">${Object.entries(E.LOCATIONS).map(([k, loc]) => `<article class="card"><h3>${loc.name}</h3><p>${loc.description}</p><div class="cost">${money(loc.price * (1 + state.turn * .007))}</div><p>Lease only · 1% of purchase price in seasonal ground rent. Warehouse construction costs an additional $15,000.</p><button type="button" data-action="land" data-location="${k}"${disabled(state.ending || state.distress || state.plots.length >= 6 || state.cash < Math.round(loc.price * (1 + state.turn * .007)))}>Acquire lease</button></article>`).join('')}</div><h3 class="subheading">Your properties</h3>${state.plots.length ? `<div class="cards">${state.plots.map(p => `<article class="card"><p class="eyebrow">Property No. ${p.id}</p><h3>${E.LOCATIONS[p.location].name}</h3><p>${p.built ? `Warehouse · ${180 + (p.upgrades.includes('expansion') ? 120 : 0)} spaces` : p.building ? 'Under construction · opens next season' : 'Undeveloped lease'}</p>${!p.built && !p.building ? `<button type="button" data-action="build" data-id="${p.id}"${disabled(state.ending || state.distress || state.cash < 15000 || E.activeProjects(state) >= (state.manager ? 2 : 1))}>Build warehouse · $15,000</button>` : ''}${p.built ? `<div class="upgrade-list">${Object.entries(E.UPGRADES).map(([k, u]) => p.upgrades.includes(k) ? `<span class="installed">✓ ${u.name}</span>` : `<button type="button" data-action="upgrade" data-id="${p.id}" data-upgrade="${k}" title="${u.description}"${disabled(state.ending || state.distress || state.cash < u.price)}><span>${u.name}</span><span>${money(u.price)}</span></button>`).join('')}</div><details><summary>Improvement benefits</summary>${Object.values(E.UPGRADES).map(u => `<p><strong>${u.name}:</strong> ${u.description}</p>`).join('')}<p>Protection is averaged across your built warehouses.</p></details>` : ''}<p class="note">Forced sale returns 65% of property book value.</p><button type="button" class="text-button small" data-ui="liquidate" data-id="${p.id}"${disabled(state.ending)}>Liquidate this property</button></article>`).join('')}</div>` : '<p class="muted">Your house has not acquired any land yet.</p>'}<h3 class="subheading">The superintendent’s office</h3><div class="card"><h3>${state.manager ? 'A capable second pair of hands' : 'Make room for bigger ambitions'}</h3><p>${state.manager ? 'Your superintendent oversees a second project. Salary: $650 per season.' : 'Hire a superintendent for $3,000 and $650 each season. The house can supervise two construction projects or public contracts at once.'}</p>${!state.manager ? `<button type="button" data-action="manager"${disabled(state.ending || state.distress || state.cash < 3000)}>Hire superintendent · $3,000</button>` : ''}</div>`;
  }
  function tenderCard(c, active) {
    const cost = E.contractCost(state, c);
    return `<article class="card"><div class="commodity-header"><p class="eyebrow">${active ? 'In progress' : 'Government tender'}</p><span class="badge">${c.major ? 'Major' : 'Local'}</span></div><h3>${E.PROJECTS[c.type].name}</h3><p>${E.PROJECTS[c.type].description}</p><div class="detail"><span>Total government payment</span><strong>${money(c.reward)}</strong></div><div class="detail"><span>Performance bond</span><strong>${money(c.bond)}</strong></div><div class="detail"><span>Work per season</span><strong>${c.cement} cement + ${money(c.labour)}</strong></div><div class="detail"><span>Next stage cash needed</span><strong>${money(cost.cash)}</strong></div><div class="detail"><span>${active ? 'Stages completed' : 'Expected duration'}</span><strong>${active ? `${c.progress} / ${c.stages}` : `${c.stages} seasons`}</strong></div><div class="detail"><span>Complete by</span><strong>${E.date({ turn: c.deadline })}</strong></div>${active ? progress(c.progress, c.stages, 'Contract progress') : `<div class="detail"><span>Official Standing required</span><strong>${c.requirement}</strong></div>`}<div class="contract-benefit">${E.PROJECTS[c.type].benefit}</div><p class="small muted">${active ? 'Each unfinished stage pays 20% of the contract total. The final stage pays the balance and returns your bond.' : `Delivery earns +${c.major ? 16 : 10} Official Standing and +${c.major ? 12 : 8} Public Trust.`}</p>${active ? `<button type="button" class="text-button small" data-ui="abandon" data-id="${esc(c.id)}"${disabled(state.ending)}>Abandon contract</button>` : `<button type="button" data-ui="contract" data-id="${esc(c.id)}"${disabled(state.ending || state.distress || state.official < c.requirement || state.cash < c.bond || !state.plots.some(p => p.built) || E.activeProjects(state) >= (state.manager ? 2 : 1))}>Post bond & accept</button>`}</article>`;
  }
  function works() {
    return `<div class="section-heading"><div><p class="eyebrow">The public works office</p><h2>Build a city. Earn its confidence.</h2><p>Fixed-price contracts reward delivery. Keep enough cash to fund each stage before payment.</p></div><span class="badge">${E.activeProjects(state)} / ${state.manager ? 2 : 1} slots</span></div>${state.contracts.length ? `<h3 class="subheading">Under your supervision</h3><div class="cards">${state.contracts.map(c => tenderCard(c, true)).join('')}</div>` : ''}<h3 class="subheading">Open tenders</h3><div class="cards">${state.tenders.map(c => tenderCard(c, false)).join('')}</div><p class="note">Missing cement is bought automatically at a 12% spot premium plus freight. Cargo arriving this season can supply the work. Storms and insufficient cash can delay stages; contracts include two buffer seasons. Default or abandonment forfeits the bond, costs an additional 5% penalty, and damages your standing. Major tenders begin in 1855.</p><h3 class="subheading">A changing harbour</h3><div class="cards">${Object.values(E.PROJECTS).map(p => `<div class="card"><h4>${p.name}</h4><div class="cost">${Math.round(E.reduction(state, p.effect) * 100)}%</div><p>${p.effect === 'demand' ? 'Greater market depth' : p.effect === 'flood' ? 'Lower stored-cargo flood losses' : p.effect === 'labour' ? 'Lower fixed operating costs' : `Lower ${p.effect} charges`} · ${state.city[p.effect]} improvements</p></div>`).join('')}</div><p class="note">Each improvement contributes 8%, capped at 28% per category. Other merchant houses occasionally complete projects too.</p>`;
  }
  function standingPanel() {
    return `<div class="section-heading"><div><p class="eyebrow">Commerce & public life</p><h2>The road to Government House</h2><p>Wealth opens doors. A sustained record earns the appointment.</p></div></div><div class="notice"><h3>An alternate-history ambition</h3><p>Become Governor by satisfying every requirement for four consecutive seasons. Appointments are reviewed at the end of each year. Reliable everyday business builds only a modest baseline; public works and civic service carry you further.</p></div><div class="requirements">${E.appointment(state).map(r => `<div class="requirement"><div class="detail"><span>${r.met ? '✓ ' : ''}${r.label}</span><strong>${r.money ? money(r.current) : Math.round(r.current * 10) / 10} / ${r.money ? money(r.target) : r.target}</strong></div>${progress(r.current, r.target, r.label)}</div>`).join('')}</div><h3 class="subheading">Two kinds of confidence</h3><div class="cards"><div class="card"><h3>Official Standing</h3><p>Complete contracts, meet financial obligations, and assist public supply. Everyday reliability rises only to 25. Failed contracts and opium route incidents damage your record.</p></div><div class="card"><h3>Public Trust</h3><p>Deliver useful works, supply food relief, and support workers. Routine fair dealing rises only to 20. Opium commerce damages trust; holding it also postpones your eight-season transition out of the trade.</p></div></div>${eventMarkup()}<p class="note">Hong Kong Tycoon is alternate history. The appointment path is a game rule. Opium’s colonial legality varied by route and period; official approval did not remove its community harms. Dollar values and public-project terms are balance abstractions.</p>`;
  }
  function chronicle() {
    return `<div class="section-heading"><div><p class="eyebrow">The merchant’s chronicle</p><h2>A record of the house</h2><p>The latest 160 entries, preserved in your save file.</p></div>${state.report ? '<button type="button" data-ui="report">Last seasonal report</button>' : ''}</div><div class="report-summary"><div><span class="eyebrow">Highest net worth</span><strong>${money(state.stats.bestWorth)}</strong></div><div><span class="eyebrow">Unrecovered cargo losses</span><strong>${money(state.stats.losses)}</strong></div></div><ol class="chronicle">${state.log.map(l => `<li><time>${E.date({ turn: l.turn })}</time><p class="${l.tone === 'bad' ? 'negative' : l.tone === 'good' ? 'positive' : ''}">${esc(l.text)}</p></li>`).join('')}</ol>`;
  }
  function updateQuotes() {
    if (tab !== 'exchange') return;
    for (const k of Object.keys(E.GOODS)) {
      const node = $(`#quote-${k}`);
      if (!node) continue;
      const qty = quantities[k];
      const valid = Number.isSafeInteger(qty) && qty > 0 && qty <= 1000000;
      node.textContent = valid ? `Order ${money(E.buyQuote(state, k, qty))} · Sale ${money(E.sellQuote(state, k, qty))}${qty > state.stock[k] ? ' (not enough held)' : ''}` : 'Enter a positive whole number of units.';
      const buy = $(`[data-trade="buy"][data-good="${k}"]`);
      const sell = $(`[data-trade="sell"][data-good="${k}"]`);
      buy.disabled = Boolean(!valid || state.ending || state.distress || E.buyQuote(state, k, qty) > state.cash || E.usedSpace(state) + qty * E.GOODS[k].space > E.capacity(state, true));
      sell.disabled = Boolean(!valid || state.ending || qty > state.stock[k]);
    }
  }
  function render() {
    renderLedger(); renderAlerts(); renderBulletin();
    for (const button of document.querySelectorAll('.tabs [data-tab]')) {
      if (button.dataset.tab === tab) button.setAttribute('aria-current', 'page');
      else button.removeAttribute('aria-current');
    }
    $('#panel').innerHTML = ({ exchange, estate, works, standing: standingPanel, ledger: chronicle })[tab]();
    updateQuotes();
  }
  function showReport() {
    if (!state.report) return;
    const r = state.report;
    modal(`${r.season} · Closing report`, `${state.ending ? `<p class="eyebrow">${state.ending === 'governor' ? 'Your appointment is confirmed' : 'The campaign has concluded'}</p>` : ''}<div class="report-summary"><div><span class="eyebrow">Operating expenses</span><strong>${money(r.expense)}</strong></div><div><span class="eyebrow">Cash movement at close</span><strong class="${r.cashChange >= 0 ? 'positive' : 'negative'}">${signed(r.cashChange)}</strong></div></div><ul class="report-list">${r.entries.map(t => `<li>${esc(t)}</li>`).join('')}</ul><p class="note">Cash movement covers seasonal resolution, excluding orders and sales you made earlier. It is not a profit figure.</p>${state.distress ? `<p class="negative">${money(-state.cash)} remains overdue. Raise cash before continuing.</p>` : ''}`, '<button type="button" class="primary" data-ui="close">Return to the house</button>');
  }
  function bank() {
    const room = Math.max(0, E.creditLimit(state) - state.debt);
    modal('The merchant’s bank', `<p class="muted">Secured credit is backed by 45% of property book value and 25% of stored cargo value. Official Standing of 25 unlocks an extra $10,000.</p><div class="report-summary"><div><span class="eyebrow">Available credit</span><strong>${money(room)}</strong></div><div><span class="eyebrow">Outstanding debt</span><strong>${money(state.debt)}</strong></div></div><p class="note">Interest: 2.5% each season, included in operating expenses. The credit limit governs new borrowing; falling collateral does not trigger an automatic margin call.</p><div class="bank"><div><label for="borrow-amount">New loan amount</label><input id="borrow-amount" type="number" min="1" step="1" value="${Math.max(1, Math.min(10000, room))}"><button type="button" data-ui="borrow"${disabled(state.ending || room < 1)}>Borrow</button></div><div><label for="repay-amount">Principal to repay</label><input id="repay-amount" type="number" min="1" step="1" value="${Math.max(1, Math.min(10000, state.debt, state.cash))}"><button type="button" data-ui="repay"${disabled(state.ending || state.distress || state.debt < 1)}>Repay</button></div></div>`);
  }
  function newHouse(first = false) {
    modal(first ? 'Your ship has arrived.' : 'Establish a new trading house', `<svg class="intro-art" viewBox="0 0 520 105" role="img" aria-label="A sailing vessel enters Victoria Harbour"><path class="solid-art" d="M0 80 55 55 98 70 155 28 203 61 255 41 318 77 386 54 435 70 490 45 520 69V100H0Z"></path><path class="line-art" d="M0 90H520M0 96H160M280 99H520M80 85 60 72H218L202 85ZM145 12V72M145 15 96 63H145ZM152 26 187 63H152ZM99 22V69M96 27 76 62H96ZM245 80V60H264V80M275 80V53H304V80M322 80V64H351V80M365 80V46H392V80M416 80V59H454V80"></path></svg><p>Spring 1852. You land in Hong Kong with <strong>$100,000</strong>, a name to make, and eighteen years to leave your mark.</p><p class="muted small">Trade rice, tea, cement, and opium. Build your stores and the city around them. Become Governor, endure to 1870, or lose the house to your creditors.</p><form id="new-form" class="new-form"><label>Name of your trading house<input id="new-name" name="house" maxlength="60" value="Victoria Trading Company" required autocomplete="off"></label><label>Campaign seed <span class="muted">Same seed + same decisions = same history</span><input id="new-seed" name="seed" maxlength="64" value="${first ? 'Victoria-1852' : `Harbour-${Math.floor(Math.random() * 100000)}`}" required autocomplete="off"></label>${!first || saveBlocked ? '<p class="small negative">Starting a new house replaces the autosave on this device. Export the current campaign first if you wish to keep it.</p>' : ''}<button type="submit" class="primary">Sign the founding papers</button></form><p class="note">No account, installation, or connection required. Autosaves stay in this browser; export a save to move between devices.</p>`);
  }
  function guide() {
    modal('The merchant’s handbook', `<div class="guide-grid"><div><h3>1. Establish your house</h3><p>Start with a $35,000 lease-and-warehouse package, or choose a location on the Estate page. Your warehouse opens next season.</p></div><div><h3>2. Keep cash in reserve</h3><p>Try 50 tea and 30 rice for your first shipment. Keep $20,000–$25,000 for expenses and surprises. “Budget max” reserves current commitments only.</p></div><div><h3>3. Trade across seasons</h3><p>New orders cannot be sold immediately. Close the season to receive cargo, then sell or hold it. Supplier prices change each season; sell margins differ by commodity.</p></div><div><h3>4. Build a legacy</h3><p>Use trade profits to fund public works. Meet all Standing-page requirements for four seasons and pass the annual review to become Governor.</p></div></div><details><summary>Weather, storage & opium</summary><p>Storm risk is 10% in Spring, 30% in Summer, 18% in Autumn, and 4% in Winter. Weather can damage stored and incoming cargo. Rice and tea deteriorate in store; cement is vulnerable to damp. Improvements protect stored goods.</p><p>Opium route incidents affect 65% of the shipment, plus any weather losses. Base incident risk is 16% before 1858 and 9% afterward, reduced by watchmen. Opium purchases and sales lower Public Trust, and holding it postpones appointment eligibility.</p></details><details><summary>Contracts & working capital</summary><p>Post a bond, then fund labour and cement before receiving milestone payments. Missing cement is bought automatically at a premium; keep stock to avoid that premium. Smaller contracts take three stages and major contracts take four. One manager can supervise one active project, or two with a superintendent.</p><p>Work pauses if you cannot fund it. Two buffer seasons allow for delays. Default forfeits the bond, adds a 5% penalty, and removes 15 Official Standing and 8 Public Trust.</p></details><details><summary>Debt & bankruptcy</summary><p>Debt charges 2.5% seasonal interest. A negative cash balance means an obligation is overdue. You can sell goods, borrow within your limit, or liquidate property at 65% of book value. Choose bankruptcy only when you cannot rescue the house.</p></details><details><summary>Endings & save files</summary><p>The campaign runs from Spring 1852 through Winter 1869. All final obligations resolve before survival is awarded as 1870 begins. Governor appointment requires eight years, $350,000 net worth, 75 Official Standing, 60 Public Trust, four completed contracts including two major projects, eight seasons out of opium, and four consecutive qualifying seasons.</p><p>Every decision is autosaved when browser storage is available. Export and import JSON saves to back up or transfer a campaign. Local saves are editable; this is a single-player game without a competitive leaderboard.</p></details><p class="note">This is an alternate-history game, not an economic reconstruction. Prices use abstract silver dollars. Colonial office and public welfare are represented as separate measures of reputation.</p>`, '<button type="button" class="primary" data-ui="close">Back to business</button>');
  }
  function exportSave() {
    try {
      const blob = new Blob([E.serialize(state)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = `hong-kong-tycoon-${state.turn}-${state.seed.replace(/[^a-z0-9-]/gi, '-').slice(0, 30)}.json`;
      document.body.append(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      toast('Save exported. Keep this file to restore your house.');
    } catch (error) { toast(error.message); }
  }
  document.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button || button.disabled) return;
    const d = button.dataset;
    if (d.tab) {
      tab = d.tab; render();
      $(`.tabs [data-tab="${tab}"]`).focus();
    } else if (d.trade) {
      const qty = quantities[d.good];
      if (d.good === 'opium' && d.trade === 'buy') confirm('An opium consignment', `<p>Order ${qty} units for <strong>${money(E.buyQuote(state, 'opium', qty))}</strong>?</p><p class="muted">This trade lowers Public Trust, exposes the cargo to uninsured route losses, and restarts the eight-season transition required for appointment.</p>`, () => dispatch({ type: 'buy', good: d.good, qty }, 'Order entered in the ledger.'), 'Place order');
      else dispatch({ type: d.trade, good: d.good, qty }, d.trade === 'buy' ? 'Order entered. Cargo arrives next season.' : 'Sale completed. Cash is in the ledger.');
    } else if (d.action) {
      const action = { type: d.action };
      if (d.id) action.id = Number(d.id);
      if (d.location) action.location = d.location;
      if (d.upgrade) action.upgrade = d.upgrade;
      if (d.choice) action.choice = d.choice;
      dispatch(action, 'The house ledger has been updated.');
    } else if (d.ui) {
      switch (d.ui) {
        case 'close': closeModal(); break;
        case 'confirm': { const run = confirmAction; closeModal(); if (run) run(); break; }
        case 'guide': guide(); break;
        case 'new': newHouse(); break;
        case 'export': exportSave(); break;
        case 'import': $('#import-file').click(); break;
        case 'bank': bank(); break;
        case 'report': showReport(); break;
        case 'borrow': case 'repay': {
          const amount = Number($(`#${d.ui}-amount`).value);
          if (dispatch({ type: d.ui, amount }, 'Bank transaction completed.')) bank();
          break;
        }
        case 'max-buy': {
          const budget = Math.max(0, state.cash - E.commitments(state));
          const free = Math.floor((E.capacity(state, true) - E.usedSpace(state)) / E.GOODS[d.good].space);
          let qty = Math.max(0, Math.min(free, Math.floor(budget / E.buyQuote(state, d.good, 1))));
          while (qty > 0 && E.buyQuote(state, d.good, qty) > budget) qty--;
          quantities[d.good] = qty; $(`#qty-${d.good}`).value = qty; updateQuotes(); break;
        }
        case 'all': quantities[d.good] = state.stock[d.good]; $(`#qty-${d.good}`).value = quantities[d.good]; updateQuotes(); break;
        case 'contract': {
          const c = state.tenders.find(c => c.id === d.id);
          confirm('Accept the government tender?', `<p><strong>${E.PROJECTS[c.type].name}</strong> requires a ${money(c.bond)} bond now and approximately ${money(E.contractCost(state, c).cash)} in cash for its next stage.</p><p class="muted">The house pays costs before receiving each milestone payment. Keep a buffer for rising cement prices and weather delays.</p>`, () => dispatch({ type: 'contract', id: d.id }, 'Contract awarded. Work begins at season close.'), 'Post performance bond'); break;
        }
        case 'abandon': confirm('Abandon this public work?', '<p>Your bond will be forfeited, a 5% contract penalty becomes payable, and Official Standing and Public Trust will fall.</p>', () => dispatch({ type: 'abandon', id: d.id }), 'Abandon contract'); break;
        case 'liquidate': confirm('Liquidate this property?', '<p>The property and its improvements will be sold at 65% of book value. Remaining warehouses must have room for all stored and incoming cargo.</p>', () => dispatch({ type: 'liquidate', id: Number(d.id) }), 'Sell property'); break;
        case 'bankrupt': confirm('Close the house for good?', '<p>This ends your campaign in bankruptcy. You can still return to the ledger to sell assets or arrange credit.</p>', () => dispatch({ type: 'bankrupt' }), 'Declare bankruptcy'); break;
        case 'end': {
          const reserve = state.cash - E.commitments(state);
          const next = E.date({ turn: state.turn + 1 });
          confirm(`Close ${E.date(state)}?`, `<p>Pay <strong>${money(E.operating(state))}</strong> in house expenses, resolve cargo arrivals and public works, and advance to <strong>${next}</strong>.</p><div class="reserve ${reserve < 0 ? 'warning' : ''}"><p>Cash after estimated commitments, before cargo claims and project payments</p><strong>${money(reserve)}</strong></div>${reserve < 0 ? '<p class="negative small">You may face an overdue balance or paused contract. Consider selling stock or borrowing first.</p>' : ''}${state.event && !state.event.resolved ? '<p class="note">An unanswered seasonal appeal will expire.</p>' : ''}`, () => dispatch({ type: 'end' }), 'Close the season'); break;
        }
      }
    }
  });
  document.addEventListener('input', event => {
    if (event.target.dataset.qty) { quantities[event.target.dataset.qty] = Number(event.target.value); updateQuotes(); }
  });
  document.addEventListener('change', event => {
    if (event.target.id === 'insurance') dispatch({ type: 'insurance', enabled: event.target.checked });
  });
  document.addEventListener('submit', event => {
    if (event.target.id !== 'new-form') return;
    event.preventDefault();
    state = E.newGame($('#new-seed').value, $('#new-name').value);
    saveBlocked = false;
    tab = 'exchange'; save(); closeModal(); render();
    toast('Your founding papers are signed. Welcome to Victoria Harbour.');
  });
  $('#import-file').addEventListener('change', async event => {
    const file = event.target.files[0];
    event.target.value = '';
    if (!file) return;
    try {
      if (file.size > 1000000) throw new Error('Save file is too large.');
      const imported = E.deserialize(await file.text());
      confirm('Restore this trading house?', `<p>Load <strong>${esc(imported.name)}</strong> in ${E.date(imported)} with ${money(imported.cash)} cash?</p><p class="muted">This replaces the current autosave. Export your current house first if you want to keep both.</p>`, () => {
        state = imported; saveBlocked = false; tab = 'exchange'; save(); render(); toast('Trading house restored.');
      }, 'Restore save');
    } catch (error) { toast(error.message); }
  });
  $('#modal').addEventListener('cancel', () => { confirmAction = null; });
  render();
  if (!recovered) newHouse(true);
})();
