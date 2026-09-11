"""Optional browser integration checks. Run with: uv run --with playwright python test/browser_smoke.py"""
from pathlib import Path
import json
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = Path(os.environ.get("TYCOON_SCREENSHOTS", "/var/folders/rj/s_47yf3s6v9cplqypdcsv4l80000gn/T/opencode"))
CHROME = os.environ.get("CHROME_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def read_save(page):
    return page.evaluate("JSON.parse(localStorage.getItem('hong-kong-tycoon-save-v1'))")


def close_season(page):
    page.locator('[data-ui="end"]').click()
    page.locator('[data-ui="confirm"]').click()
    assert page.locator('#modal-title').inner_text().endswith('Closing report')
    page.locator('#modal [data-ui="close"]').last.click()


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME if Path(CHROME).exists() else None, headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1050}, color_scheme="light", reduced_motion="reduce")
    errors, requests = [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('request', lambda request: requests.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
    page.goto((ROOT / 'index.html').as_uri())
    page.locator('#new-name').fill('Jade Harbour & Co.')
    page.locator('#new-seed').fill('browser-smoke')
    page.locator('#new-form button[type="submit"]').click()
    assert page.locator('#house-name').inner_text() == 'Jade Harbour & Co.'
    page.locator('[data-action="establish"]').click()
    assert read_save(page)['cash'] == 65000
    page.locator('#qty-tea').fill('50')
    page.locator('[data-trade="buy"][data-good="tea"]').click()
    page.locator('#qty-rice').fill('30')
    page.locator('[data-trade="buy"][data-good="rice"]').click()
    assert read_save(page)['stock']['tea'] == 0
    assert page.locator('[data-trade="sell"][data-good="tea"]').is_disabled()
    page.screenshot(path=str(ARTIFACTS / 'tycoon-desktop.png'), full_page=True)
    close_season(page)
    assert read_save(page)['turn'] == 1
    assert read_save(page)['stock']['tea'] > 0
    page.locator('[data-action="event"][data-choice="help"]').click()
    assert read_save(page)['stats']['relief'] == 1
    page.locator('[data-ui="all"][data-good="tea"]').click()
    page.locator('[data-trade="sell"][data-good="tea"]').click()
    assert read_save(page)['stock']['tea'] == 0

    # Complete an actual contract through browser controls.
    page.locator('.tabs [data-tab="works"]').click()
    page.locator('[data-ui="contract"]').first.click()
    page.locator('[data-ui="confirm"]').click()
    for _ in range(6):
        if not read_save(page)['contracts']:
            break
        close_season(page)
    assert read_save(page)['completed'] == 1

    # Credit operations preserve current season and survive reload.
    page.locator('[data-ui="bank"]').click()
    page.locator('#borrow-amount').fill('5000')
    page.locator('[data-ui="borrow"]').click()
    assert read_save(page)['debt'] == 5000
    page.locator('#repay-amount').fill('2500')
    page.locator('[data-ui="repay"]').click()
    assert read_save(page)['debt'] == 2500
    page.keyboard.press('Escape')
    saved = read_save(page)
    page.reload()
    assert not page.locator('#modal').is_visible()
    assert read_save(page) == saved

    # All departments fit common desktop/tablet/mobile sizes in both themes.
    for scheme in ['light', 'dark']:
        page.emulate_media(color_scheme=scheme)
        for width in [1440, 1024, 768, 390, 320]:
            page.set_viewport_size({"width": width, "height": 900})
            for tab in ['exchange', 'estate', 'works', 'standing', 'ledger']:
                page.locator(f'.tabs [data-tab="{tab}"]').click()
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), f'Overflow: {scheme}, {width}, {tab}'
            if width == 390:
                page.locator('.tabs [data-tab="exchange"]').click()
                page.screenshot(path=str(ARTIFACTS / f'tycoon-mobile-{scheme}.png'), full_page=True)

    page.set_viewport_size({"width": 1440, "height": 1050})
    page.emulate_media(color_scheme='light')
    # JSON exports are portable, and hostile names are rendered only as text.
    with page.expect_download() as download_info:
        page.locator('[data-ui="export"]').click()
    download = download_info.value
    with open(download.path(), encoding='utf-8') as exported_file:
        exported = json.load(exported_file)
    assert exported == saved
    exported['name'] = '<img src=x onerror="window.injected=true">'
    page.locator('#import-file').set_input_files({"name": "portable-save.json", "mimeType": "application/json", "buffer": json.dumps(exported).encode()})
    page.locator('[data-ui="confirm"]').click()
    assert page.locator('#house-name').inner_text() == exported['name']
    assert page.evaluate('window.injected') is None

    # Malformed imports must leave the current campaign intact.
    before = read_save(page)
    page.locator('#import-file').set_input_files({"name": "bad.json", "mimeType": "application/json", "buffer": b'{"version":1}'})
    page.wait_for_function("document.querySelector('#toast').textContent.startsWith('Cannot load save:')")
    assert read_save(page) == before

    # Exercise victory and distress UI using engine-produced fixture saves.
    fixture = page.evaluate('''() => {
      let s = Tycoon.act(Tycoon.newGame('victory'), {type:'establish'});
      s = Tycoon.act(s, {type:'end'});
      Object.assign(s, {turn:35,cash:500000,official:90,trust:80,completed:4,majorCompleted:2,qualifying:3,lastOpium:20});
      return Tycoon.serialize(s);
    }''')
    page.locator('#import-file').set_input_files({"name": "victory.json", "mimeType": "application/json", "buffer": fixture.encode()})
    page.locator('[data-ui="confirm"]').click()
    close_season(page)
    assert read_save(page)['ending'] == 'governor'
    assert page.locator('.ending h2').inner_text() == 'His Excellency, the Governor'
    assert page.locator('[data-ui="end"]').is_disabled()
    page.screenshot(path=str(ARTIFACTS / 'tycoon-governor.png'), full_page=True)

    fixture = page.evaluate('''() => {
      let s = Tycoon.act(Tycoon.newGame('distress'), {type:'establish'});
      s = Tycoon.act(s, {type:'end'}); s.cash=0;
      return Tycoon.serialize(Tycoon.act(s, {type:'end'}));
    }''')
    page.locator('#import-file').set_input_files({"name": "distress.json", "mimeType": "application/json", "buffer": fixture.encode()})
    page.locator('[data-ui="confirm"]').click()
    assert page.locator('[data-ui="end"]').is_disabled()
    page.locator('[data-ui="bankrupt"]').click()
    page.locator('[data-ui="confirm"]').click()
    assert read_save(page)['ending'] == 'bankrupt'
    assert page.locator('.ending h2').inner_text() == 'The House Falls Silent'

    assert errors == [], errors
    assert requests == [], requests
    browser.close()
    print('PASS: browser trading, contracts, bank, persistence, export/import, hostile saves, endings, and 50 responsive/theme layouts; no JavaScript errors or network requests.')
