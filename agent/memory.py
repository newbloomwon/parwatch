"""The agent's long-term memory — SurrealDB Agent Memory.

Mock mode (no keys): remembers to a local JSON file so the loop still works.
Live mode: stores/recall via the Agent Memory REST API.

  store :  POST {endpoint}/api/v1/{context}/facts   {"text": ...}
  recall:  POST {endpoint}/api/v1/{context}/query    {"query": ..., "k": N}
  auth  :  Authorization: Bearer <api_key>

Endpoint host + context id come from the SurrealDB Studio "API keys" view.
"""
import json
import ssl
import urllib.request
import config

_LOCAL = config.HERE / ".memory.jsonl"

# macOS python.org builds often lack root certs for urllib, causing
# CERTIFICATE_VERIFY_FAILED. Use certifi's bundle when available.
try:
    import certifi
    _SSL = ssl.create_default_context(cafile=certifi.where())
except Exception:  # noqa: BLE001
    _SSL = ssl.create_default_context()


def remember(text):
    """Store one fact (e.g. an order the agent placed)."""
    if not config.SURREAL_LIVE:
        with open(_LOCAL, "a") as f:
            f.write(json.dumps({"text": text}) + "\n")
        return "local"

    endpoint = config.get("SURREAL_MEM_ENDPOINT").rstrip("/")
    ctx = config.get("SURREAL_MEM_CONTEXT")
    key = config.get("SURREAL_MEM_KEY")
    # Plain text fact — verified to return 200 and be recallable. (A "scopes"
    # value must be pre-registered or the API 400s; "infer: full" also works but
    # is heavier. Plain is the reliable choice.)
    body = json.dumps({"text": text}).encode()
    req = urllib.request.Request(
        f"{endpoint}/api/v1/{ctx}/facts", data=body, method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30, context=_SSL) as r:
            r.read()
        return "surreal"
    except Exception as e:  # noqa: BLE001
        print(f"[memory] store failed ({e}); wrote local copy.")
        with open(_LOCAL, "a") as f:
            f.write(json.dumps({"text": text}) + "\n")
        return "local"


def recall(query, k=5):
    """Recall past facts matching a query. Returns a list of text snippets."""
    if not config.SURREAL_LIVE:
        if not _LOCAL.exists():
            return []
        return [json.loads(l)["text"] for l in _LOCAL.read_text().splitlines()][-k:]

    endpoint = config.get("SURREAL_MEM_ENDPOINT").rstrip("/")
    ctx = config.get("SURREAL_MEM_CONTEXT")
    key = config.get("SURREAL_MEM_KEY")
    body = json.dumps({"query": query, "k": k}).encode()
    req = urllib.request.Request(
        f"{endpoint}/api/v1/{ctx}/query", data=body, method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30, context=_SSL) as r:
            data = json.loads(r.read())
        # Response shape may vary by version; pull text fields defensively.
        hits = data.get("results") or data.get("hits") or data.get("facts") or []
        out = []
        for h in hits:
            out.append(h.get("text") if isinstance(h, dict) else str(h))
        # Drop any throwaway test facts so the demo recall stays clean.
        out = [t for t in out if t and "test order" not in t.lower()]
        return out[:k]
    except Exception as e:  # noqa: BLE001
        print(f"[memory] recall failed ({e}).")
        return []
