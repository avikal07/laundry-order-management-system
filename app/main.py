"""
main.py — FastAPI application entry point.

Start the server with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import orders, dashboard

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Mini Laundry Order Management System",
    description=(
        "A simple REST API to manage laundry orders. "
        "Create orders, update their status, filter them, "
        "and view dashboard statistics — all in memory."
    ),
    version="1.0.0",
)

# Allow all origins (fine for local development / no auth)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Register routers
# ---------------------------------------------------------------------------

app.include_router(orders.router)
app.include_router(dashboard.router)

# ---------------------------------------------------------------------------
# Root health-check
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    """Quick health-check endpoint."""
    return {"message": "Laundry Order Management System is running 🧺"}
