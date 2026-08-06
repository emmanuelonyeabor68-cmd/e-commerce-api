# E-Commerce API

A backend API for e-commerce built with Django and Django REST Framework. Handles product catalog, cart management, and order checkout, with JWT authentication and admin-only product control.

## Features

- **Product catalog** — public read access, admin-only create/update
- **Cart** — authenticated users can add, view, and manage cart items
- **Checkout** — converts a cart into a permanent order, with price/name snapshotting so historical orders never change even if product prices change later
- **Stock safety** — checkout uses database row locking (`select_for_update`) inside an atomic transaction to prevent overselling when multiple users check out the same product simultaneously
- **Order management** — customers see only their own orders; staff can view all orders and update order status (e.g. pending → shipped)
- **Authentication** — JWT-based, with a custom login endpoint
- **Image uploads** — product images via multipart form-data

## Tech Stack

- Python / Django / Django REST Framework
- PostgreSQL (production) / SQLite (local development)
- JWT authentication
- Deployment target: Render (API) + Neon (PostgreSQL)

## API Overview

| Endpoint | Method | Access |
|---|---|---|
| `/api/v1/products/` | GET | Public |
| `/api/v1/products/` | POST | Admin only |
| `/api/v1/cart/` | GET | Authenticated |
| `/api/v1/cart-items/` | POST | Authenticated |
| `/api/v1/orders/checkout/` | POST | Authenticated |
| `/api/v1/orders/` | GET | Own orders (staff see all) |
| `/api/v1/orders/{id}/` | PATCH | Admin only (status updates) |
| `/auth/v1/login/` | POST | Public |

## Setup

```bash
git clone <repo-url>
cd <project-folder>
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Notes

- Product prices and names are snapshotted onto each order at checkout time, so past orders remain accurate even if a product's price changes later.
- Stock deduction and stock validation happen inside the same atomic transaction, using row-level locking, to prevent race conditions during concurrent checkouts. This requires PostgreSQL in production — SQLite does not enforce row locking the same way.
- Image uploads work locally via Django's default file storage. Production deployment requires a persistent storage backend (e.g. Cloudinary), since platforms like Render use ephemeral disks that are wiped on redeploy.

## Roadmap

- Payment integration
- Google OAuth login
- Cloud image storage (Cloudinary)
- Deployment (Render + Neon)
- Google OAuth login
- Cloud image storage (Cloudinary)
- Deployment (Render + Neon)
