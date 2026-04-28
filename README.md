# 🧺 Mini Laundry Order Management System

A clean, minimal REST API built with **FastAPI** + **in-memory storage** (no database needed).

---

## Project Structure

```
laundry_app/
├── index.html
├── assets/                    # Screenshots used in README
│ ├── create_new_order.png
│ ├── dashboard.png
│ ├── endpoints_overview.png
│ ├── orders.png
│ └── schemas_models.png
├── app/
│   ├── main.py               # FastAPI app, middleware, router registration
│   ├── models.py             # Pydantic schemas (request/response shapes)
│   ├── db/
│   │   └── store.py          # In-memory dictionary (our "database")
│   ├── services/
│   │   └── order_service.py  # Business logic (create, list, update, stats)
│   └── routes/
│       ├── orders.py         # POST /orders, GET /orders, PATCH /orders/{id}/status
│       └── dashboard.py      # GET /dashboard
├── requirements.txt
└── README.md
```

---

## Setup & Run

### 1. Clone / unzip the project

```bash
cd laundry_app
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at → **http://127.0.0.1:8000**

### 5. Explore interactive docs

- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc      → http://127.0.0.1:8000/redoc

---

## Simple Frontend

A basic frontend (`index.html`) is included for quick interaction.

### Features:
- Create orders via form
- View all orders
- Update order status
- View dashboard stats

### How to use:

1. Start backend:
   ```bash
   uvicorn app.main:app --reload
---

## 📸 Backend (Swagger UI)

### API Endpoints Overview
![Endpoints](assets/endpoints_overview.png)

### Request/Response Schemas
![Schemas](assets/schemas_models.png)

---

## 🎨 Frontend (index.html)

### Create Order
![Create Order](assets/create_new_order.png)

### Orders List & Status Update
![Orders](assets/orders.png)

### Dashboard
![Dashboard](assets/Dashboard.png)

---

## API Endpoints

### Health Check

```
GET /
```

**Response:**
```json
{ "message": "Laundry Order Management System is running 🧺" }
```

---

### Create an Order

```
POST /orders
```

**Request body:**
```json
{
  "customer_name": "Rahul Sharma",
  "phone_number": "9876543210",
  "garments": [
    { "garment_type": "SHIRT",   "quantity": 3, "price_per_item": 30 },
    { "garment_type": "PANT",    "quantity": 2, "price_per_item": 50 },
    { "garment_type": "BLANKET", "quantity": 1, "price_per_item": 150 }
  ]
}
```

**Response `201`:**
```json
{
  "order_id": "ORD-0001",
  "customer_name": "Rahul Sharma",
  "phone_number": "9876543210",
  "garments": [
    { "garment_type": "SHIRT",   "quantity": 3, "price_per_item": 30 },
    { "garment_type": "PANT",    "quantity": 2, "price_per_item": 50 },
    { "garment_type": "BLANKET", "quantity": 1, "price_per_item": 150 }
  ],
  "total_bill": 390.0,
  "status": "RECEIVED",
  "created_at": "2024-01-15T10:30:00+00:00",
  "updated_at": "2024-01-15T10:30:00+00:00"
}
```

---

### List / Filter Orders

```
GET /orders
GET /orders?status=READY
GET /orders?customer_name=Rahul
GET /orders?phone_number=9876543210
GET /orders?status=PROCESSING&customer_name=Priya
```

**Available query parameters:**

| Param           | Type   | Description                                            |
|-----------------|--------|--------------------------------------------------------|
| `status`        | string | Filter by status: `RECEIVED`, `PROCESSING`, `READY`, `DELIVERED` |
| `customer_name` | string | Partial, case-insensitive match                        |
| `phone_number`  | string | Exact match                                            |

**Response `200`:** Array of order objects (newest first).

---

### Update Order Status

```
PATCH /orders/{order_id}/status
```

**Example:** `PATCH /orders/ORD-0001/status`

**Request body:**
```json
{ "status": "PROCESSING" }
```

Valid statuses: `RECEIVED` → `PROCESSING` → `READY` → `DELIVERED`

**Response `200`:** Updated order object.

**Response `404`** if order not found:
```json
{ "detail": "Order 'ORD-9999' not found" }
```

---

### Dashboard Summary

```
GET /dashboard
```

**Response `200`:**
```json
{
  "total_orders": 5,
  "total_revenue": 1850.0,
  "orders_per_status": {
    "RECEIVED":   1,
    "PROCESSING": 2,
    "READY":      1,
    "DELIVERED":  1
  }
}
```

---

## Validation Rules

| Field           | Rule                                                         |
|-----------------|--------------------------------------------------------------|
| `customer_name` | Cannot be blank                                              |
| `phone_number`  | Must be a valid 10-digit Indian mobile number (6–9 prefix)  |
| `garments`      | Must contain at least one item                               |
| `quantity`      | Must be ≥ 1                                                  |
| `price_per_item`| Must be > 0                                                  |

---

## Supported Garment Types

`SHIRT`, `PANT`, `SUIT`, `SAREE`, `JACKET`, `BLANKET`, `BEDSHEET`, `OTHER`

---

## Notes

- Data is stored **in memory** — it resets when the server restarts.
- No authentication is required.
- Total bill is auto-calculated as `sum(quantity × price_per_item)` per garment.
- Order IDs are sequential: `ORD-0001`, `ORD-0002`, …


---

## License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Avikal Singh**  
Backend Developer (Python | FastAPI) • AI-First Builder  

- 🧺 Built: Mini Laundry Order Management System (FastAPI + In-Memory Storage + Simple Frontend)  
- 🤖 Approach: AI-assisted development (scaffolding, debugging, UI generation)  
- 💻 Focus: Backend APIs, system design, and rapid prototyping  

- GitHub: [avikal07](https://github.com/avikal07)  
- LinkedIn: [Avikal Singh](https://linkedin.com/in/avikal-singh)

---