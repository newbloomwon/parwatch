# ParWatch — key setup checklist

**The one file you edit:** `agent/.env` (already created). Paste each value
**after the `=`** — no quotes, no spaces. Blank lines stay in mock mode.
After any change: `cd agent && python3 run.py`. The top of the output shows
`LIVE ●` vs `mock ○` for each service.

Open the file:
```bash
open -e ~/Documents/WhereIsIt/agent/.env
```

---

## 1. SurrealDB Agent Memory  (no pip install needed)

You're on the **Agent Memory** product (studio.surrealdb.com) — the newer thing,
not classic SurrealDB. Ignore any earlier "Root Authentication / Connect → Python
wss://" instructions; those were for classic SurrealDB and don't apply.

- [ ] **KEY** — the `sp-…` key you copied ("Copy your API key now"). That IS the
      right value. → paste into `SURREAL_MEM_KEY=`
- [ ] **CONTEXT** — already filled in for you (`06gkar91j9q357nsv0u3ro9a9k`, from
      your Studio URL). Nothing to do unless you switch contexts.
- [ ] **ENDPOINT** — on the same **API Keys** page, find the context **host/base URL**
      (look near the key, or open the **Python** quick-start panel at the bottom —
      the base URL is in the sample). It looks like `https://<id>.<region>.surreal.cloud`.
      → paste into `SURREAL_MEM_ENDPOINT=`
- [ ] Verify: `python3 run.py` → top line shows `SurrealDB LIVE ●`, and after you
      approve an order it says "Remembered in SurrealDB."

_Paste here for your own notes:_ ENDPOINT = `________________`

## 2. Anchor Browser

- [ ] Copy the **Default API Key** (`sk-xxxx…xxxx`) from Anchor → **API Keys**.
      → paste into `ANCHOR_API_KEY=`
- [ ] `pip install playwright && playwright install chromium`
- [ ] **Host the supplier page** (needed because Anchor is a *cloud* browser and
      can't open a file on your laptop): drag `../mock-supplier.html` onto
      **app.netlify.com/drop**, copy the URL it gives you.
      → paste into `SUPPLIER_URL=`
- [ ] Verify: `python3 run.py` → `Anchor LIVE ●`, browse step names your URL.

_Paste here:_ SUPPLIER_URL = `________________`

## 3. Arize Phoenix

- [ ] Copy the **System API Key** from Phoenix → Settings → **API Keys**
      (your "ParWatch" key). → paste into `PHOENIX_API_KEY=`
- [ ] `PHOENIX_COLLECTOR_ENDPOINT` is already filled (`https://app.phoenix.arize.com`).
- [ ] `pip install arize-phoenix-otel`
- [ ] Verify: `python3 run.py` → `Arize/Phoenix LIVE ●`; spans appear under
      **Tracing** in the Phoenix UI.

## 4. ElevenLabs

- [ ] The key is under **Settings → API Keys** (the key icon in the left rail, or
      your avatar menu → API Keys) — **not** "Profile". Copy it.
      → paste into `ELEVENLABS_API_KEY=`
- [ ] **Voice**: a default voice id is already filled in, so you can skip this.
      To pick your own: **Voices** → open a voice → copy its **Voice ID** →
      paste into `ELEVENLABS_VOICE_ID=`.
- [ ] `pip install elevenlabs`
- [ ] Verify: `python3 run.py` → `ElevenLabs LIVE ●`; the nudge plays in an
      ElevenLabs voice instead of the Mac `say` voice.

## 5. AWS — optional, skip for now

Only needed if you host a model on Bedrock. The agent's decision is rule-based,
so you don't need it. Revisit only with spare time on the day.

---

## Tonight's "done"

`python3 run.py` shows at least:
```
SurrealDB  LIVE ●
Arize/Phoenix LIVE ●
ElevenLabs LIVE ●
```
Anchor can stay `mock ○` until you host the supplier page — that's the only step
that needs hosting, and it's safe to finish in the room.
