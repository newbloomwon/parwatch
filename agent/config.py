"""Central config. Loads .env if present; every value is optional.

A missing key is not an error — it just means that integration runs in mock
mode. `status()` prints which parts are live so you can see it at a glance.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # the WhereIsIt/ folder that holds the seed + mock supplier

# Load .env by hand (no dependency needed) so mock mode stays stdlib-only.
_envfile = HERE / ".env"
if _envfile.exists():
    for line in _envfile.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.split("#", 1)[0].strip())


def get(name, default=""):
    return os.environ.get(name, default).strip()


# Convenience flags: is each integration configured for real mode?
# SurrealDB Agent Memory (REST): needs endpoint host + context id + key.
SURREAL_LIVE = bool(get("SURREAL_MEM_ENDPOINT") and get("SURREAL_MEM_CONTEXT") and get("SURREAL_MEM_KEY"))
ANCHOR_LIVE = bool(get("ANCHOR_API_KEY") and get("SUPPLIER_URL"))
# Live if an endpoint is set. Cloud also needs PHOENIX_API_KEY; a local
# Phoenix (http://localhost:6006) needs no key.
PHOENIX_LIVE = bool(get("PHOENIX_COLLECTOR_ENDPOINT"))
VOICE_LIVE = bool(get("ELEVENLABS_API_KEY"))

SEED_FILE = ROOT / "seed-inventory.json"
MOCK_SUPPLIER = ROOT / "mock-supplier.html"


def status():
    def mark(live):
        return "LIVE ●" if live else "mock ○"
    print("ParWatch config:")
    print(f"  SurrealDB   {mark(SURREAL_LIVE)}")
    print(f"  Anchor      {mark(ANCHOR_LIVE)}")
    print(f"  Arize/Phoenix {mark(PHOENIX_LIVE)}")
    print(f"  ElevenLabs  {mark(VOICE_LIVE)}")
