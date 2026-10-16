#!/usr/bin/env python3
"""ParWatch — autonomous F&B restock agent.

The full loop:  CHECK -> DETECT -> BROWSE -> DECIDE -> ASK (human gate) -> VOICE
Every step is traced (Arize/Phoenix live, console otherwise).

Run it:
    python3 run.py            # interactive: asks you to approve each order
    python3 run.py --auto     # non-interactive: auto-declines (for a dry run)

With no .env it runs fully in mock mode against the local seed + supplier page.
Fill .env one key at a time to turn each step real — nothing else changes.
"""
import sys
import config
import db
import browse
import decide
import voice
import memory
from trace import tracer, flush

AUTO = "--auto" in sys.argv


def bar():
    print("\n" + "=" * 56)


def main():
    print("\n  PARWATCH — where is it?!\n")
    config.status()

    # 0) RECALL — what does the agent remember from past runs?
    with tracer.span("recall") as s:
        past = memory.recall("recent restock orders", k=3)
        s.set("summary", f"{len(past)} past orders recalled")
    if past:
        print("\n  Memory — recent orders ParWatch remembers:")
        for p in past:
            print(f"    · {p}")

    # 1) CHECK — read current stock
    with tracer.span("check") as s:
        inventory = db.load_inventory()
        s.set("items", len(inventory))
        s.set("summary", f"{len(inventory)} items read")

    # 2) BROWSE — get live supplier prices + availability
    with tracer.span("browse") as s:
        catalog, source = browse.fetch_supplier_catalog()
        s.set("supplier", source)
        s.set("summary", f"{len(catalog)} products from {source}")

    # 3) DETECT + DECIDE — reason over the two
    with tracer.span("decide") as s:
        drafts, holds, healthy = decide.decide(inventory, catalog)
        total = decide.order_total(drafts)
        s.set("drafts", len(drafts))
        s.set("holds", len(holds))
        s.set("summary", f"{len(drafts)} to order (${total}), {len(holds)} held")

    # Report
    bar()
    print(f"  {len(healthy)} healthy · {len(drafts)} below par & orderable · {len(holds)} need attention")
    bar()

    for h in holds:  # the safeguard: surfaced, never auto-ordered
        with tracer.span("hold") as s:
            s.hold(h["reason"])
            s.set("item", h["name"])
        print(f"  ⚠  {h['name']}  ({h['have']}/{h['par']}) — {h['reason']}. HELD, not ordered.")

    if not drafts:
        print("\n  Nothing to reorder. Watching.\n")
        tracer.print_table()
        return

    print(f"\n  Draft order — {len(drafts)} items, ${total} total:")
    for d in drafts:
        tag = "critical" if d["critical"] else "low"
        print(f"    • {d['order_qty']}× {d['name']:<26} @ ${d['unit_price']:<6} = ${d['line_total']:<7} [{tag}]")

    # 4) ASK — the human approval gate. The agent NEVER buys on its own.
    names = [d["name"] for d in drafts]
    headline = next((n for n in names if "Rye" in n), names[0])
    headline = headline.replace(" 750ml", "").replace(" 1L", "").lower()
    voice.say(f"Heads up — {len(drafts)} items are below par, including {headline}. "
              f"I can reorder everything from BoroughBev for ${total}. "
              f"Want me to place the order?")

    with tracer.span("approval") as s:
        if AUTO:
            approved = False
            print("\n  [--auto] no human present → declined (safe default).")
        else:
            ans = input(f"\n  Approve this ${total} order? [y/N] ").strip().lower()
            approved = ans in ("y", "yes")
        s.set("approved", approved)
        s.set("summary", "human approved" if approved else "declined / held")

    if approved:
        with tracer.span("place_order") as s:
            items_txt = ", ".join(f"{d['order_qty']}x {d['name']}" for d in drafts)
            where = memory.remember(
                f"Approved restock order of {len(drafts)} items (${total}) from BoroughBev: {items_txt}."
            )
            s.set("summary", f"order placed + remembered ({where})")
        print(f"\n  ✓ Order placed: {len(drafts)} items, ${total}. Remembered in SurrealDB.")
    else:
        print("\n  ✗ Not placed. Left as a pending draft for you.")

    tracer.print_table()


if __name__ == "__main__":
    main()
    flush()  # make sure Phoenix receives all spans before we exit
