# Hong Kong Tycoon

A complete, offline browser game about establishing a trading house in Hong Kong in 1852. Begin with $100,000; trade across 72 seasons, build public works, and pursue appointment as Governor before 1870.

## Play

Open **`index.html`** in a modern browser. The file contains the entire game, including its styles and engine. No installation, server, account, or network connection is needed.

For local HTTP hosting, run this from this directory:

```sh
npm run serve
```

Then visit **http://localhost:1852**.

For static deployment, upload **`index.html`** to the desired directory on any static web host. All paths are self-contained, so hosting under a subdirectory also works. No environment variables, backend, CDN, or build service are required.

### A suggested first season

1. Name your house and sign the founding papers.
2. Choose **Establish the house** for a $20,000 town lease and $15,000 warehouse.
3. Order approximately **50 tea and 30 rice**, leaving a substantial cash reserve.
4. Close Spring 1852. Your warehouse opens and cargo arrives in Summer.
5. Sell stored cargo or hold it, consult the next outlook, and plan your next orders.

The in-game **How to play** handbook explains all major rules. The ledger shows cash after upcoming obligations; keep extra reserves for weather and project delays.

## Implemented mechanics

- Spring 1852 through Winter 1869, followed by the Spring 1870 epilogue.
- Four commodities: rice, tea, cement, and opium.
- Next-season cargo arrivals, finite market depth, seasonal prices, mean reversion, harvest and demand shocks, and storm-driven price pressure.
- Weather losses, perishable inventory, insured cargo, and distinct uninsured opium route exposure.
- Three land locations, six-plot limit, warehouse construction and five improvements.
- Public wharf, road, drainage, waterworks, and market contracts, including major projects.
- Bonds, labour/material costs, milestone payments, delay buffers, defaults, and final settlement of unfinished projects.
- Permanent city benefits capped at 28% per category; occasional rival-led improvements.
- Official Standing and Public Trust, finite civic opportunities, and opium transition requirements.
- Secured credit, seasonal interest, emergency property liquidation, and a player-controlled bankruptcy declaration after an unpaid obligation.
- Governor, survival, and bankruptcy endings.
- Seeded simulation, browser autosave, validated JSON export/import, and a 160-entry chronicle.
- Responsive newspaper-and-ledger interface, system light/dark themes, keyboard controls, reduced-motion support, and accessible dialogs.

### Saving

The game attempts to autosave every successful action to browser `localStorage`. Some browsers restrict storage on local files; the status below **Close the season** reports availability. Use **Export save** to back up a campaign or move it between browsers and devices. Imported saves replace the autosave only after confirmation.

Saves contain all simulation state, including the random-number-generator state. The same seed and decisions reproduce the same results in this version. Exported saves are editable, as expected for a local single-player game; there is no trusted leaderboard.

### Endings

Governor appointment requires:

- Eight years established.
- Official Standing of at least 75 and Public Trust of at least 60.
- Net worth of at least $350,000.
- Four completed public contracts, including two major projects.
- Eight seasons out of opium trading and holding.
- Four consecutive qualifying seasonal closes, with appointment at an annual review.

Reaching 1870 solvent earns the survival ending. At the final close, unfinished public contracts are settled as defaults before survival is checked. New tenders stop when their minimum duration would extend beyond the campaign.

Negative cash is an overdue obligation, not an immediate game over. Sell cargo, borrow within your secured limit, or sell property. The house cannot advance another season until the balance is covered. Bankruptcy is an explicit final action.

## Source structure

| File | Purpose |
| --- | --- |
| `index.html` | Generated, portable game; deploy or open this file |
| `engine.js` | Standalone deterministic simulation, usable in a browser or Node.js |
| `app.js` | Browser rendering, controls, dialogs, and save handling |
| `style.css` | Responsive light/dark newspaper styling |
| `shell.html` | Application document and build insertion points |
| `build.cjs` | Dependency-free bundler |
| `test/engine.test.cjs` | Rules, boundaries, save validation, and campaign regressions |
| `test/balance.cjs` | 100-seed experiments for three trading policies |
| `test/browser_smoke.py` | Optional real-browser interaction and layout checks |

### Build and test

Requires Node.js 20 or newer; there are no npm dependencies to install.

```sh
npm run build
npm test
npm run balance
```

Edit the source files, then rebuild. Do not edit `index.html` directly because the build replaces it.

The engine exports `newGame`, `act`, quote/ledger helpers, `serialize`, and `deserialize`. `act(state, action)` returns a new state; rejected actions leave the original untouched. It has no dependency on the DOM, filesystem, network, or wall clock. A future terminal interface can reuse it directly:

```js
const game = require('./engine.js');
let state = game.newGame('Victoria-1852', 'Jade Harbour & Co.');
state = game.act(state, { type: 'establish' });
state = game.act(state, { type: 'buy', good: 'tea', qty: 50 });
state = game.act(state, { type: 'end' });
console.log(game.date(state), state.cash, state.stock);
```

Optional browser verification uses Python Playwright and Chrome/Chromium:

```sh
# Set this to an existing directory for screenshots.
export TYCOON_SCREENSHOTS=/tmp
uv run --with playwright python test/browser_smoke.py
```

The script uses the standard macOS Chrome installation when available. Set `CHROME_PATH` for another Chrome location; otherwise install Playwright Chromium for the active Python environment. Screenshot output is diagnostic and is not needed for deployment.

## Balance and historical framing

This is a first playable balance, supported by deterministic simulations and browser checks, rather than a claim of exhaustive human playtesting. The balance script compares cautious tea trading, concentrated opium trading, and civic construction using explicit repeatable policies. Cash-flow distress is reported separately from bankruptcy because a human may rescue the house by borrowing or liquidating assets.

Prices, silver-dollar values, contract terms, and governorship requirements are game abstractions. The merchant-to-Governor path is deliberately alternate history. Official approval and public welfare are separate measures. Opium regulation varied by market and period; the game abstracts route risks and their change around 1858.
