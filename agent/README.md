# ParWatch agent

Minimal runnable F&B restock agent. Runs **end-to-end with zero keys** in mock
mode, then turns real one key at a time.

## Run it now (mock mode, no setup)

```bash
cd agent
python3 run.py          # interactive — asks you to approve the order
python3 run.py --auto   # dry run — auto-declines
```

You'll see: 10 items read → supplier catalog scraped (from the local
`mock-supplier.html`) → 5 drafts + 1 held (olives, supplier out of stock) →
voice nudge → approval gate → Arize-style trace table.

## The loop

`CHECK` (db.py) → `BROWSE` (browse.py) → `DECIDE` (decide.py) →
`ASK` human (run.py) → `VOICE` (voice.py), all wrapped in spans (trace.py).

| File | Job | Mock mode | Live mode |
|---|---|---|---|
| `db.py` | inventory = agent memory | reads `../seed-inventory.json` | SurrealDB |
| `browse.py` | supplier prices/stock | parses `../mock-supplier.html` | Anchor Browser + Playwright |
| `decide.py` | reasoning (rule-based, auditable) | same | same |
| `voice.py` | spoken nudge | prints + macOS `say` | ElevenLabs |
| `trace.py` | observability | console table | Arize/Phoenix OTEL |

## Going live

1. `cp .env.example .env` and fill in keys (see the key walkthrough).
2. `pip install -r requirements.txt` (only what you're turning on).
3. For Anchor: host `mock-supplier.html` at a public URL, set `SUPPLIER_URL`,
   and put the Anchor connect endpoint in `ANCHOR_CDP_URL`.
4. Re-run `python3 run.py`. `config.status()` at the top shows LIVE ● vs mock ○.

The decision logic never changes between mock and live, so what you rehearse is
what you demo.

## Safeguard

The agent **never places an order on its own.** It drafts, speaks the nudge, and
waits for an explicit human `y`. Items below par whose supplier is out of stock
are **held and surfaced**, never guessed. That's the judged behavior — keep it.
