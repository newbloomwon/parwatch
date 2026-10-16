"""The reasoning step. For each item below par, cross-reference the live
supplier catalog and decide:

  - below par  + supplier IN stock   -> DRAFT an order (qty = par - current)
  - below par  + supplier OUT of stock -> HOLD (needs human attention; never guess)
  - at/above par                      -> nothing to do

This is deliberately rule-based: it's auditable, it can't hallucinate a price,
and judges can see exactly why each decision was made. (An LLM can be layered on
top for a natural-language rationale, but the *decision* stays grounded in data.)
"""


def decide(inventory, catalog):
    drafts, holds, healthy = [], [], []
    for it in inventory:
        short = it["current_qty"] < it["par"]
        if not short:
            healthy.append(it)
            continue
        supply = catalog.get(it["supplier_sku"])
        need = it["par"] - it["current_qty"]
        if supply and supply["stock"] == "in":
            drafts.append({
                "name": it["name"],
                "sku": it["supplier_sku"],
                "have": it["current_qty"],
                "par": it["par"],
                "unit": it["unit"],
                "order_qty": need,
                "unit_price": supply["price"],
                "line_total": round(need * supply["price"], 2),
                "critical": it["current_qty"] <= it["par"] * 0.5,
            })
        else:
            holds.append({
                "name": it["name"],
                "sku": it["supplier_sku"],
                "have": it["current_qty"],
                "par": it["par"],
                "reason": "supplier out of stock" if supply else "not found at supplier",
            })
    drafts.sort(key=lambda d: (not d["critical"], d["name"]))
    return drafts, holds, healthy


def order_total(drafts):
    return round(sum(d["line_total"] for d in drafts), 2)
