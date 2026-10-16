# WhereIsIt?! — F&B Restock Agent (HackSprint)

An "observability agent" that watches a restaurant's bar & kitchen inventory, browses a
supplier when something drops below par, drafts a reorder, and **stops for human approval
before buying.** Branded with the hand-drawn eye logo (the agent that *watches*).

## Files here

| File | What it is |
|---|---|
| `BUILD-PLAN.md` | The full event-day plan: agent loop, sponsor mapping, 10:00–3:30 timeline, 3-min pitch. |
| `seed-inventory.json` | 10 realistic bar/kitchen items with par levels. 6 are **below par** (restock triggers); 4 are fine. Load into SurrealDB at start. |
| `mock-supplier.html` | Self-contained supplier catalog for Anchor Browser to scrape. SKUs match the seed file. One item (olives) is **out of stock** so the agent must reason about availability, not just price. |

## Demo-safe design choices

- **seed data is pre-tuned:** rye whiskey (3/12), vermouth (1/6), club soda (6/24), limes (1/3),
  olives (2/4, and the supplier is OUT), espresso beans (2/8) all fire. Clean, repeatable demo.
- **mock supplier removes live-web risk:** open `mock-supplier.html` locally or host it; the agent
  browses a stable page that can't rate-limit or flake on stage. Each row carries `data-sku`,
  `data-price`, `data-stock` mirroring the visible text, so scraping is robust.
- **the olive case is the safeguard moment:** item below par BUT supplier out of stock → agent
  should flag "can't reorder, needs attention" rather than invent an order. Good thing to show judges.

## To wire up (event morning)

1. Load `seed-inventory.json` → SurrealDB (agent memory).
2. Point Anchor Browser at `mock-supplier.html` (host it, or a real login-free supplier later).
3. Match on `supplier_sku`; pull price + availability.
4. Draft order for below-par + in-stock items → **approval gate** → ElevenLabs voice nudge.
5. Trace every step in Arize.
