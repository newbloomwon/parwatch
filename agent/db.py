"""Inventory source. Reads ../seed-inventory.json.

Note: inventory lives in the seed file (it's simple structured state). SurrealDB
is used for the agent's *memory* of past decisions/orders — see memory.py — which
is what SurrealDB Agent Memory is designed for and what the "Best Use of SurrealDB"
prize rewards.
"""
import json
import config


def load_inventory():
    data = json.loads(config.SEED_FILE.read_text())
    return data["items"]
