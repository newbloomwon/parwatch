"""The agent's hands: fetch live supplier prices + availability.

Mock mode: parses the local ../mock-supplier.html (its rows carry
data-sku / data-price / data-stock, so parsing is exact and dependency-free).

Live mode: drives Anchor Browser to open SUPPLIER_URL (your hosted copy of
mock-supplier.html, or a real supplier site) and scrape the same fields.

Returns a dict keyed by SKU:  { "SPR-RYE-750": {"price": 21.5, "stock": "in"}, ... }
"""
import re
import config


def _parse_local_html(html):
    catalog = {}
    for row in re.findall(r"<tr[^>]*data-sku=.*?</tr>", html, re.S):
        sku = re.search(r'data-sku="([^"]+)"', row)
        price = re.search(r'data-price="([^"]+)"', row)
        stock = re.search(r'data-stock="([^"]+)"', row)
        if sku and price and stock:
            catalog[sku.group(1)] = {"price": float(price.group(1)), "stock": stock.group(1)}
    return catalog


def fetch_supplier_catalog():
    if not config.ANCHOR_LIVE:
        html = config.MOCK_SUPPLIER.read_text()
        return _parse_local_html(html), "BoroughBev (local mock)"

    # ── Live Anchor Browser ───────────────────────────────────────────
    # Anchor gives you a cloud browser you connect to over CDP with Playwright.
    # Grab the connect endpoint (ANCHOR_CDP_URL) from the Anchor dashboard.
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        print("[browse] playwright not installed; using local mock. `pip install playwright`")
        html = config.MOCK_SUPPLIER.read_text()
        return _parse_local_html(html), "BoroughBev (local mock)"

    url = config.get("SUPPLIER_URL")
    key = config.get("ANCHOR_API_KEY")
    # Anchor requires creating a session first (REST), then connecting to the
    # cdp_url it returns. The old ?apiKey= shortcut is gone. ANCHOR_CDP_URL, if
    # you set it, overrides this (e.g. a session you made by hand).
    cdp = config.get("ANCHOR_CDP_URL")
    try:
        if not cdp:
            cdp = _create_anchor_session(key)
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(cdp)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            html = page.content()
            browser.close()
        catalog = _parse_local_html(html)  # same markup as the hosted page
        print(f"[browse] Anchor live — scraped {len(catalog)} products from {url}")
        return catalog, f"BoroughBev (Anchor · {url})"
    except Exception as e:  # noqa: BLE001
        print(f"[browse] Anchor error ({e}); using local mock.")
        html = config.MOCK_SUPPLIER.read_text()
        return _parse_local_html(html), "BoroughBev (local mock)"


def _create_anchor_session(key):
    """Create an Anchor browser session and return its CDP connect URL.

    POST https://api.anchorbrowser.io/v1/sessions  (header anchor-api-key)
    -> the response carries a cdp_url to connect Playwright to.
    """
    import json
    import ssl
    import urllib.request
    try:
        import certifi
        sslctx = ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001
        sslctx = ssl.create_default_context()
    req = urllib.request.Request(
        "https://api.anchorbrowser.io/v1/sessions",
        data=json.dumps({}).encode(), method="POST",
        headers={"anchor-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30, context=sslctx) as r:
        data = json.loads(r.read())
    # cdp_url may be nested under "data"; fall back to top level.
    d = data.get("data", data)
    cdp = d.get("cdp_url") or d.get("cdpUrl") or d.get("connectionString")
    if not cdp:
        raise RuntimeError(f"no cdp_url in Anchor session response: {data}")
    return cdp
