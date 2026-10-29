# ExpiryWatch API — System Architecture

## 1. System Overview
ExpiryWatch is a synchronous REST API designed for small pharmacy and patent medicine shop owners. It provides secure, multi-tenant inventory tracking to prevent medical stock from expiring unnoticed. The system is designed for local or lightweight cloud deployment.

## 2. Technology Stack
*   **Web Framework:** FastAPI (Python 3.10+)
*   **Database:** PostgreSQL 16 (Relational DB)
*   **ORM & Migrations:** SQLAlchemy 2.0 & Alembic
*   **Authentication:** PyJWT (Stateless Bearer Tokens) & Passlib (Bcrypt)
*   **Security & Performance:** `slowapi` (Rate Limiting) & `fastapi.middleware.cors`
*   **Testing:** Pytest & HTTPX (In-memory SQLite isolated testing)
*   **Environment:** Docker (Database containerization) & Virtualenv

## 3. Core Architectural Decisions

### 3.1 Multi-Tenant Isolation (Row-Level Security)
Instead of physical database separation, the system uses logical isolation. Every core entity (`Product`, `Supplier`, `Batch`) is linked to a `User` via an `owner_id`. The application layer enforces strict ownership validation (`verify_product_ownership`) before permitting read, update, or delete operations.

### 3.2 Atomic Inventory Transactions
Stock changes are strictly append-only. The `batches.quantity_remaining` column is updated dynamically via the `adjustments` table. To prevent race conditions when multiple users adjust the same batch simultaneously, the API utilizes database-level row locking (`.with_for_update()`) during the adjustment transaction.

### 3.3 Stateless Authentication
The API does not use session cookies. It relies on short-lived (60 min) JWT access tokens. This keeps the backend stateless, allowing it to restart or scale horizontally without losing user login sessions.

### 3.4 Rate Limiting & Defense
The `/auth/login` endpoint is protected against brute-force credential stuffing by an in-memory rate limiter (`slowapi`), capped at 5 requests per minute per IP address.

## 4. Directory Structure Layering
The application strictly separates concerns across defined layers:
*   `app/routers/`: HTTP transport layer. Handles route definitions, path parameters, and status codes.
*   `app/schemas/`: Data validation layer. Pydantic models validate incoming JSON payloads and format outgoing responses.
*   `app/models/`: Database layer. SQLAlchemy ORM models define table structures and foreign key relationships.
*   `app/database.py` & `app/limiter.py`: Core infrastructure and dependency injection setups.