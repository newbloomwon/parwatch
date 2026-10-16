#!/bin/bash
# Local Phoenix fallback — run this in its OWN terminal tab and leave it open.
# It starts a local Phoenix trace UI at http://localhost:6006.
#
# Then, to point the agent at it, set this line in .env:
#     PHOENIX_COLLECTOR_ENDPOINT=http://localhost:6006
# (and you can leave PHOENIX_API_KEY blank for local).
#
# To switch back to cloud, set:
#     PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com/s/parwatch

echo "Installing/updating Phoenix (first run only)…"
pip install -q arize-phoenix

echo "Starting Phoenix at http://localhost:6006  (Ctrl-C to stop)"
phoenix serve
