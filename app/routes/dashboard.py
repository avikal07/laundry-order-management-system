"""
routes/dashboard.py — API route handler for the dashboard summary.

Routes defined here:
  GET /dashboard → get_dashboard
"""

from fastapi import APIRouter
from app.models import DashboardResponse
from app.services import order_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard():
    """
    Return aggregate statistics:
      - total_orders      : total number of orders in the system
      - total_revenue     : sum of all order bills (₹)
      - orders_per_status : count of orders in each status
    """
    return order_service.get_dashboard()
