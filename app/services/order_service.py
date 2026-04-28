"""
services/order_service.py — Business logic layer.

All heavy lifting (ID generation, bill calculation, filtering, stats)
happens here so that route handlers stay thin and readable.
"""

from datetime import datetime, timezone
from typing import List, Optional

from app.db.store import orders_db
from app.models import OrderCreate, OrderStatus


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    """Return current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _generate_order_id() -> str:
    """
    Generate a sequential, human-readable order ID like ORD-0001.
    Finds the highest existing number and increments by 1.
    """
    if not orders_db:
        return "ORD-0001"

    # Extract the numeric part from existing IDs
    existing_numbers = [
        int(oid.split("-")[1])
        for oid in orders_db.keys()
        if oid.startswith("ORD-") and oid.split("-")[1].isdigit()
    ]
    next_number = max(existing_numbers) + 1
    return f"ORD-{next_number:04d}"


def _calculate_total(garments: list) -> float:
    """Sum up quantity × price_per_item for every garment line."""
    return sum(g.quantity * g.price_per_item for g in garments)


# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------

def create_order(payload: OrderCreate) -> dict:
    """
    Create a new order, store it in memory, and return the full record.
    """
    order_id   = _generate_order_id()
    total_bill = _calculate_total(payload.garments)
    now        = _now_iso()

    order = {
        "order_id":      order_id,
        "customer_name": payload.customer_name,
        "phone_number":  payload.phone_number,
        # Convert each GarmentItem to a plain dict for easy storage
        "garments": [g.model_dump() for g in payload.garments],
        "total_bill":    round(total_bill, 2),
        "status":        OrderStatus.RECEIVED,
        "created_at":    now,
        "updated_at":    now,
    }

    orders_db[order_id] = order
    return order


def list_orders(
    status:        Optional[str] = None,
    customer_name: Optional[str] = None,
    phone_number:  Optional[str] = None,
) -> List[dict]:
    """
    Return orders, optionally filtered by:
      • status        — exact match (case-insensitive)
      • customer_name — partial match (case-insensitive)
      • phone_number  — exact match
    """
    results = list(orders_db.values())

    if status:
        results = [o for o in results if o["status"] == status.upper()]

    if customer_name:
        query = customer_name.lower()
        results = [o for o in results if query in o["customer_name"].lower()]

    if phone_number:
        results = [o for o in results if o["phone_number"] == phone_number]

    # Return newest orders first
    results.sort(key=lambda o: o["created_at"], reverse=True)
    return results


def get_order(order_id: str) -> Optional[dict]:
    """Fetch a single order by ID, or None if not found."""
    return orders_db.get(order_id)


def update_order_status(order_id: str, new_status: OrderStatus) -> Optional[dict]:
    """
    Update the status of an existing order.
    Returns the updated order, or None if the order doesn't exist.
    """
    order = orders_db.get(order_id)
    if not order:
        return None

    order["status"]     = new_status
    order["updated_at"] = _now_iso()
    return order


# ---------------------------------------------------------------------------
# Dashboard / analytics
# ---------------------------------------------------------------------------

def get_dashboard() -> dict:
    """
    Compute aggregate statistics across all orders:
      • total_orders
      • total_revenue   (sum of total_bill for ALL orders)
      • orders_per_status
    """
    all_orders = list(orders_db.values())

    total_orders  = len(all_orders)
    total_revenue = round(sum(o["total_bill"] for o in all_orders), 2)

    # Build a count for every possible status (show 0 even if no orders)
    orders_per_status = {status.value: 0 for status in OrderStatus}
    for order in all_orders:
        status_key = order["status"]
        # status might be stored as an enum or a string
        if hasattr(status_key, "value"):
            status_key = status_key.value
        orders_per_status[status_key] = orders_per_status.get(status_key, 0) + 1

    return {
        "total_orders":      total_orders,
        "total_revenue":     total_revenue,
        "orders_per_status": orders_per_status,
    }
