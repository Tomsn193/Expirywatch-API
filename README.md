# ExpiryWatch API — Small Pharmacy Expiry Tracker

A FastAPI backend that helps owners of small pharmacies and patent medicine shops track products, suppliers, stock batches and expiry dates, so expired stock is noticed before it becomes a financial loss or a safety risk.

## Overview

Many small shops track stock informally, so items can expire unnoticed. ExpiryWatch records each delivery (a batch) with its own expiry date, keeps a full history of every stock change, and lists the batches that are about to expire.

Each owner has their own account. An owner can only see and change their own products, suppliers, batches and stock adjustments.

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy and Alembic
- PostgreSQL 16 (run locally with Docker)
- JWT bearer authentication (PyJWT) and bcrypt password hashing

## Current Status

**Week 2: feature work complete, with known limitations.** Week 2 adds authentication and ownership, suppliers, batches, stock adjustments, the expiring-soon query and one error format. Some behaviour does not yet match the intended design; see [Known limitations](#known-limitations) below.

- Week 1 (products) is tagged `week-1`.
- Week 2 will be tagged `week-2` once the known limitations are fixed.

Full endpoint details are in [`docs/api-spec.md`](docs/api-spec.md).

## Features

- Sign up and log in, with passwords stored only as bcrypt hashes
- Protected routes: every product, supplier, batch and adjustment route requires a valid token
- Ownership checks on every record
- Suppliers, with protection against deleting a supplier that still has batches
- Batches with duplicate-number checks and reference checks
- Stock changes only through adjustment records, applied inside a row-locked transaction, with a database constraint that stops stock going negative
- An expiring-soon query for batches with stock left
- One error format across the whole API, with no stack traces or SQL in responses

## Prerequisites

- Python 3.10 or newer
- Docker installed and running

## Local Setup

1. Clone the repository and move into the project directory.
2. Copy `.env.example` to a new file named `.env`.
3. Set a strong local password for `POSTGRES_PASSWORD`, and use the same value in `DATABASE_URL`.
4. Generate a JWT secret and set it as `JWT_SECRET_KEY` in `.env`:

   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(48))"
   ```

5. Start the database container:

   ```bash
   docker compose up -d
   ```

6. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

7. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

8. Apply the database migrations:

   ```bash
   alembic upgrade head
   ```

9. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

10. Open the interactive docs at <http://127.0.0.1:8000/docs>, or use the sample requests in `requests/` (see [Trying the API](#trying-the-api)).

The optional seed script (`scripts/seed_products.py`) currently fails after the Week 2 changes. See [Known limitations](#known-limitations).

## Authentication

Sign up with an email and password, then log in to receive an access token. Send the token on every protected request:

```
Authorization: Bearer <access_token>
```

- Passwords must be 8 to 72 characters.
- Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default 60).
- Login returns the same error whether the email is unknown or the password is wrong, so the API does not reveal which accounts exist.

Example login from the command line:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "owner1@example.test", "password": "demo-pass-123"}'
```

## API Overview

All routes except `GET /health`, `POST /auth/signup` and `POST /auth/login` require a bearer token.

| Method | Path | Success | Purpose |
| :--- | :--- | :--- | :--- |
| GET | `/health` | `200` | Check the API is running |
| POST | `/auth/signup` | `201` | Create an owner account |
| POST | `/auth/login` | `200` | Get an access token |
| GET | `/auth/me` | `200` | Return the logged-in owner |
| POST | `/products` | `201` | Create a product |
| GET | `/products` | `200` | List your products |
| GET | `/products/{id}` | `200` | Get one of your products |
| PUT | `/products/{id}` | `200` | Update one of your products |
| DELETE | `/products/{id}` | `204` | Delete one of your products |
| POST | `/suppliers` | `201` | Create a supplier |
| GET | `/suppliers` | `200` | List your suppliers |
| GET | `/suppliers/{id}` | `200` | Get one of your suppliers |
| PUT | `/suppliers/{id}` | `200` | Update one of your suppliers |
| DELETE | `/suppliers/{id}` | `204` | Delete a supplier with no batches |
| POST | `/batches` | `201` | Record a delivery (batch) |
| GET | `/batches` | `200` | List your batches |
| GET | `/batches/expiring-soon?days=30` | `200` | Batches with stock expiring within N days |
| GET | `/batches/{id}` | `200` | Get one batch |
| POST | `/batches/{id}/adjustments` | `201` | Record a stock change |
| GET | `/batches/{id}/adjustments` | `200` | Stock change history for a batch |

Full details, including request bodies, rules and error codes, are in `docs/api-spec.md`.

## Errors

Every error uses the same shape, and stack traces are never returned:

```json
{ "error": { "code": "PRODUCT_NOT_FOUND", "message": "Product 9999 not found" } }
```

Invalid input returns **400** (not FastAPI's default 422) with `code: "INVALID_INPUT"` and a `details` list of the failing fields. See `docs/design-decisions.md` (DEC-004, DEC-005) and the error code catalogue in `docs/api-spec.md`.

## Trying the API

The sample files are in `requests/`, for use with the VS Code "REST Client" extension:

- `auth.http`: sign up, log in, and check the current user. Copy the `access_token` from the login response into `@token`.
- `inventory.http`: create a supplier and a batch, run the expiring-soon query, and record and check stock adjustments.
- `product.http`: product CRUD. Every request in this file needs an `Authorization` header, which it does not yet include (see [Known limitations](#known-limitations)).

Do not commit real tokens or passwords. Replace the `@token` value with your own locally only.

## Environment and Security Notes

- `DATABASE_URL` and `JWT_SECRET_KEY` are read only from the environment. Keep `.env` private; it is git-ignored.
- `JWT_SECRET_KEY` must be a long random value. The placeholder in `.env.example` must be replaced. See [Known limitations](#known-limitations) for the current fallback behaviour.
- The local PostgreSQL database is bound to `127.0.0.1` and is intended for development only.
- In production, store credentials in your deployment platform's secret manager and keep the database on a private network.
- Only dummy data is used throughout this project.


## Documentation

See the `docs/` folder for the project concept, work plan, data model, API specification, design decisions, test results and logs.

## Entity Relationship Diagram (ERD)

![ExpiryWatch ERD](docs/erd.png)

## Warning

This is a learning project. Use dummy data only. Never enter real pharmacy stock records, personal customer details, or real passwords.
