# HackSprint Build Plan — F&B Restock Agent

**Event:** Daytona HackSprint w/ Arize AI (NYC) · One-day sprint
**Hacking window:** 10:00 AM → 3:30 PM (~5.5 hrs) · Finalists present 4:00 PM · 3 min each
**Judged on:** originality, technical strength, real-world impact — **plus a required safeguards slide + live "operating safely" demo**

---

## The idea (one sentence)

An autonomous agent that watches a restaurant's inventory, and when an item drops below its par level, **browses supplier sites to find price & availability, then drafts a reorder and stops for human approval before buying.**

**Brand:** reuse your hand-drawn eye logo — the "observability agent" that *watches* stock. (The eye doubles as the Arize story: it watches the agent, you watch the eye.)
**Name options:** `ParWatch` · `Mise` · `Lookout` · `ParEye` _(restaurants call stock thresholds "par levels" — lean into that term, it signals you know the domain)._

---

## The agent loop (keep it this simple)

```
1. CHECK   → read current stock + par levels        (SurrealDB = live state + agent memory)
2. DETECT  → item below par? flag it                 (reasoning step — log it)
3. BROWSE  → go to supplier site, get price/stock     (Anchor Browser = the agent's hands)
4. DECIDE  → cheapest in-stock option, draft order    (reasoning step — log it)
5. ASK     → surface draft to human, WAIT for yes/no   ← THE SAFEGUARD. Never auto-buys.
6. VOICE   → speak the nudge out loud                  (ElevenLabs)
   (every step above is traced in Arize)
```

## Sponsor → where it's used (each is a separate "Best Use of" prize)

| Sponsor | Job in the demo | Prize angle |
|---|---|---|
| **SurrealDB** | Store stock levels, par thresholds, order history = **agent memory** | They want it used *as memory* — name it that in the pitch |
| **Anchor Browser** | Agent browses supplier site(s) for price/availability | The visible "wow" — show the browser working live |
| **Arize** (Phoenix) | Trace every reasoning + tool step; show an eval/score | Most teams skip this — **your differentiator** |
| **ElevenLabs** | Voice nudge: "You're low on X, cheapest is $Y — reorder?" | Cheap to add, big demo payoff |
| **Daytona** | Run the agent in a sandbox | "Best Use of Daytona" + grand-prize credits |
| **AWS** | Model hosting / Bedrock if used | Participation-tier, optional |

**Safeguard (the judged pillar):** the agent **never completes a purchase.** It drafts, shows the full order (item, qty, supplier, price), and requires an explicit human "Approve." Say this out loud in the pitch and *demonstrate the stop.*

---

## Timeline (10:00 → 3:30)

| Time | Goal |
|---|---|
| **10:00–10:30** | Scaffold repo in Daytona. Wire SurrealDB. Seed ONE product category (e.g. 8–10 bar/kitchen items) with par levels. Drop in the eye logo. |
| **10:30–11:30** | Core loop CHECK→DETECT working against SurrealDB. Hardcode nothing you can seed. |
| **11:30–12:30** | Anchor Browser step: agent opens ONE supplier page, pulls price/stock. Pick a stable, login-free site (or a mock supplier page you host). |
| **12:30–1:00** | Lunch — keep it short. |
| **1:00–2:00** | DECIDE + ASK (approval gate) + draft-order UI. This is the money shot — make the "stop for approval" visible. |
| **2:00–2:45** | Arize tracing on every step; get one eval/score on the agent's decision. ElevenLabs voice nudge. |
| **2:45–3:15** | Polish demo path end-to-end. Rehearse the exact 3-min run once. Build fallback (recorded screen capture) in case live browsing flakes. |
| **3:15–3:30** | Submit. Breathe. |

**Scope discipline:** ONE category, ONE supplier source, ONE happy-path demo. Everything else is "future work" in the pitch.

---

## 3-minute pitch outline

1. **Hook (20s):** "Independent restaurants lose money every night they run out of a key item — and owners still check supplier sites by hand." Show the eye logo.
2. **Idea + advantages (40s):** the agent watches par levels and does the supplier legwork autonomously.
3. **Live demo (90s):** trigger a low-stock item → agent browses supplier (Anchor) → drafts order → **voice nudge (ElevenLabs)** → you click Approve. Then flip to **Arize** showing the full traced reasoning.
4. **Safeguards slide (20s):** never auto-buys; human approval gate; every decision traced & eval'd in Arize; runs sandboxed in Daytona.
5. **Market + close (10s):** "Any SMB that reorders from suppliers. We started with F&B."

---

## Pre-event prep (do tonight, not on the clock)

- [ ] Confirm sponsor accounts/API keys work: Anchor, Arize, SurrealDB, ElevenLabs, Daytona.
- [ ] Decide the supplier page you'll browse (real login-free site, or host a simple mock page so the demo can't break).
- [ ] Export the eye logo as SVG/PNG, ready to drop in.
- [ ] Decide the product category + seed data.
- [ ] Pick the name.
