"""
db/store.py — In-memory "database".

A plain Python dict acts as our data store.
Key   → order_id  (str)
Value → dict representation of the order

No persistence — data resets when the server restarts.
"""

from typing import Dict

# The single source of truth for all orders.
# Shape: { "ORD-0001": { ...order fields... }, ... }
orders_db: Dict[str, dict] = {}
