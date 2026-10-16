# ParWatch — 3-minute pitch & demo script

**Tagline:** *where is it?!* · **Links:** live dashboard → https://newbloomwon.github.io/parwatch/ · code → https://github.com/newbloomwon/parwatch

Target ~2:30. Speak a touch slower than feels natural. Lines in **bold** are the
prize-winning beats — hit them clearly.

---

### SHOT 1 — dashboard, Scene 1 "Watching" · (0:00–0:18)
> "Independent restaurants lose money every single night they run out of a key item — and most owners still check supplier prices by hand.
> This is ParWatch. That's its eye — it quietly watches every par level. Right now, everything's stocked. Nothing needs you."

### SHOT 2 — Terminal: `python3 run.py` · (0:18–0:52)
> "When I run the agent, watch the top: SurrealDB, Anchor, Arize, and ElevenLabs — all live.
> [point to 'Anchor live — scraped 10 products'] It just browsed a real supplier with Anchor Browser and pulled live prices.
> [point to 'Memory'] And it already remembers the last order it placed — that's SurrealDB agent memory."

### SHOT 3 — the draft + held olives · (0:52–1:28)
> "Five items are below par. It's drafted a reorder for four-eighty-two forty-five.
> But look at this one — [point to olives] below par, and the supplier's out of stock. **So the agent held the order instead of guessing.** That restraint is the whole point.
> [let voice play] And it tells you out loud, with ElevenLabs."

### SHOT 4 — type `y` at the prompt · (1:28–1:45)
> "Here's the safeguard: **it never buys on its own. It waits for a human.** [type y] One keystroke — approved, placed, and remembered."

### SHOT 5 — Phoenix, parwatch project → Spans · (1:45–2:12)
> "And every step you just saw — the browse, the reasoning, the decision to hold — is **traced in Arize Phoenix. Judges can audit exactly why the agent did what it did. Nothing is a black box.**"

### SHOT 6 — back to dashboard, click "Approved" scene · (2:12–2:30)
> "We started with bar and kitchen inventory, but this is any small business that reorders from suppliers.
> Five sponsors, one agent, a real safeguard. ParWatch — so you never have to ask *where is it?!* again."

---

### Delivery notes
- **Win-the-prize lines:** "it held the order instead of guessing" (safeguard), "traced in Arize… nothing is a black box" (observability), "it never buys on its own" (safety).
- Fumble? Just restart that shot and stitch takes — no penalty for a clean cut.
- ~2:30 leaves buffer under a 3-minute limit.

### Sponsor coverage (for the slide / Q&A)
| Sponsor | Role in ParWatch |
|---|---|
| **SurrealDB** | Agent memory — remembers and recalls past orders |
| **Anchor Browser** | The agent's hands — browses the supplier for live prices/stock |
| **Arize Phoenix** | Observability — traces every reasoning + tool step |
| **ElevenLabs** | Voice — speaks the restock nudge |
| **Daytona / AWS** | Sandbox / compute for running the agent |

### The safeguard (say it plainly)
ParWatch **never places an order on its own.** It drafts, speaks the nudge, and
waits for an explicit human approval. An item below par whose supplier is out of
stock is **held and surfaced**, never guessed. That is the judged behavior.
