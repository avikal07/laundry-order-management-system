"""
models.py — Pydantic schemas for request/response validation.
All data shapes used by the API live here.
"""

from pydantic import BaseModel, field_validator, ConfigDict
from typing import List, Optional
from enum import Enum
import re


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class OrderStatus(str, Enum):
    RECEIVED   = "RECEIVED"
    PROCESSING = "PROCESSING"
    READY      = "READY"
    DELIVERED  = "DELIVERED"


class GarmentType(str, Enum):
    SHIRT    = "SHIRT"
    PANT     = "PANT"
    SUIT     = "SUIT"
    SAREE    = "SAREE"
    JACKET   = "JACKET"
    BLANKET  = "BLANKET"
    BEDSHEET = "BEDSHEET"
    OTHER    = "OTHER"


# ---------------------------------------------------------------------------
# Garment — a single line-item inside an order
# ---------------------------------------------------------------------------

class GarmentItem(BaseModel):
    garment_type:   GarmentType
    quantity:       int
    price_per_item: float   # price in ₹ (or whatever currency)

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity must be at least 1")
        return v

    @field_validator("price_per_item")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Price per item must be greater than 0")
        return v


# ---------------------------------------------------------------------------
# Order — request body sent by the client
# ---------------------------------------------------------------------------

class OrderCreate(BaseModel):
    customer_name: str
    phone_number:  str
    garments:      List[GarmentItem]

    @field_validator("customer_name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Customer name cannot be blank")
        return v

    @field_validator("phone_number")
    @classmethod
    def phone_must_be_valid(cls, v: str) -> str:
        # Accept 10-digit numbers, optionally prefixed with +91 or 0
        cleaned = re.sub(r"[\s\-()]", "", v)
        if not re.fullmatch(r"(\+91|0)?[6-9]\d{9}", cleaned):
            raise ValueError(
                "Invalid phone number. Expected a 10-digit Indian mobile number "
                "(e.g. 9876543210 or +919876543210)"
            )
        return cleaned

    @field_validator("garments")
    @classmethod
    def garments_must_not_be_empty(cls, v: List[GarmentItem]) -> List[GarmentItem]:
        if not v:
            raise ValueError("Order must contain at least one garment")
        return v


# ---------------------------------------------------------------------------
# Status update — request body for PATCH /orders/{id}/status
# ---------------------------------------------------------------------------

class StatusUpdate(BaseModel):
    status: OrderStatus


# ---------------------------------------------------------------------------
# Order — full record stored in memory and returned to clients
# ---------------------------------------------------------------------------

class OrderResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    order_id:      str
    customer_name: str
    phone_number:  str
    garments:      List[GarmentItem]
    total_bill:    float
    status:        OrderStatus
    created_at:    str   # ISO-8601 string; no datetime import needed in routes
    updated_at:    str


# ---------------------------------------------------------------------------
# Dashboard summary
# ---------------------------------------------------------------------------

class DashboardResponse(BaseModel):
    total_orders:      int
    total_revenue:     float
    orders_per_status: dict   # { "RECEIVED": 3, "PROCESSING": 1, … }
