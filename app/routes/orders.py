"""
routes/orders.py — API route handlers for order management.

Routes defined here:
  POST   /orders              → create_order
  GET    /orders              → list_orders
  PATCH  /orders/{id}/status  → update_status
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models import OrderCreate, OrderResponse, StatusUpdate
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


# ---------------------------------------------------------------------------
# POST /orders — Create a new order
# ---------------------------------------------------------------------------

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(payload: OrderCreate):
    """
    Create a new laundry order.

    - Validates customer name, phone number, and garment list.
    - Auto-calculates the total bill.
    - Returns the created order with a unique order ID.
    """
    order = order_service.create_order(payload)
    return order


# ---------------------------------------------------------------------------
# GET /orders — List all orders (with optional filters)
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[OrderResponse])
def list_orders(
    status:        Optional[str] = Query(None, description="Filter by status: RECEIVED | PROCESSING | READY | DELIVERED"),
    customer_name: Optional[str] = Query(None, description="Partial match on customer name"),
    phone_number:  Optional[str] = Query(None, description="Exact match on phone number"),
):
    """
    Retrieve all orders, optionally filtered by status, customer name, or phone.

    Examples:
      GET /orders
      GET /orders?status=READY
      GET /orders?customer_name=Rahul
      GET /orders?phone_number=9876543210
    """
    orders = order_service.list_orders(
        status=status,
        customer_name=customer_name,
        phone_number=phone_number,
    )
    return orders


# ---------------------------------------------------------------------------
# PATCH /orders/{order_id}/status — Update order status
# ---------------------------------------------------------------------------

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_status(order_id: str, payload: StatusUpdate):
    """
    Update the status of a specific order.

    Valid transitions (no restriction enforced — any status → any status):
      RECEIVED → PROCESSING → READY → DELIVERED
    """
    updated = order_service.update_order_status(order_id, payload.status)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"Order '{order_id}' not found",
        )
    return updated
