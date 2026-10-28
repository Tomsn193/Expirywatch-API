# ExpiryWatch API Specification

This document describes the API as it is implemented in Week 2, including the rules it enforces. 

## 1. Conventions

- **Base URL (local):** `http://127.0.0.1:8000`
- **Format:** JSON request and response bodies.
- **Authentication:** Bearer token in the `Authorization` header. See [section 2](#2-authentication).
- **Success codes:**
  - `200 OK` for retrieval and updates.
  - `201 Created` for creation.
  - `204 No Content` for deletion (no body).
- **Error codes:** `400`, `401`, `403`, `404`, `405`, `409`, `500`. Validation failures return `400`, not FastAPI's default `422`.
- **Timestamps:** `created_at` values are returned in ISO 8601 format.

### Error format

Every error uses this shape:

```json
{
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product 9999 not found"
  }
}
```

Validation errors (`400`, `INVALID_INPUT`) also include a `details` list naming each failing field:

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Validation failed",
    "details": [
      { "field": "quantity_received", "message": "Input should be greater than 0" }
    ]
  }
}
```

Unknown routes return `404 NOT_FOUND`, wrong methods return `405 METHOD_NOT_ALLOWED`, and unexpected server errors return `500 INTERNAL_ERROR` with no internal details. Internal errors are logged on the server only.

## 2. Authentication

Authentication uses JWT bearer tokens. The decision is to be recorded in `docs/design-decisions.md`.

| Setting | Value |
| :--- | :--- |
| Algorithm | `HS256` (from `JWT_ALGORITHM`) |
| Token lifetime | 60 minutes (from `ACCESS_TOKEN_EXPIRE_MINUTES`) |
| Signing secret | `JWT_SECRET_KEY`, read from the environment only |
| Token subject | The user's `id` |

### Password rules

- Length: 8 to 72 characters. (Intended limit is 72 bytes. See [known gaps](#8-known-gaps).)
- Stored only as a bcrypt hash. The plain password is never stored or logged.

### Endpoints

#### `POST /auth/signup`

Creates an owner account.

Request:

```json
{ "email": "owner1@example.test", "password": "demo-pass-123" }
```

| Response | When |
| :--- | :--- |
| `201 Created` | Account created. Body contains `id`, `email`, `role` and `created_at`. The password and its hash are never returned. |
| `400 INVALID_INPUT` | Missing field, or password outside 8 to 72 characters. |
| `409 EMAIL_TAKEN` | The email is already registered. |

Emails are stored in lowercase.

#### `POST /auth/login`

Exchanges valid credentials for a token.

Request:

```json
{ "email": "owner1@example.test", "password": "demo-pass-123" }
```

| Response | When |
| :--- | :--- |
| `200 OK` | Body contains `access_token` and `token_type: "bearer"`. |
| `400 INVALID_INPUT` | Missing field. (See [known gaps](#8-known-gaps) for password length.) |
| `401 INVALID_CREDENTIALS` | Unknown email or wrong password. Both return the same message. |

#### `GET /auth/me`

Returns the logged-in owner. Requires a token.

| Response | When |
| :--- | :--- |
| `200 OK` | Body contains `id`, `email`, `role` and `created_at`. |
| `401 UNAUTHORIZED` | Token missing, malformed, badly signed, expired, or the user no longer exists. |

### Token failures

A protected route returns `401 UNAUTHORIZED` with a `WWW-Authenticate: Bearer` header when:

- no `Authorization` header is sent,
- the header is not in the form `Bearer <token>`,
- the signature is wrong or the token is malformed,
- the token has expired, or
- the user named in the token no longer exists.

## 3. Authorisation and ownership

- **Every route except** `GET /health`, `POST /auth/signup` and `POST /auth/login` requires a valid token. Read routes require login as well as write routes. This decision is to be recorded in `docs/design-decisions.md`.
- **Ownership:** each owner can read and change only their own records.
  - Products and suppliers store an `owner_id` directly.
  - Batches belong to a product, and adjustments belong to a batch, so ownership is checked through the parent product.
- **Missing versus not yours:** a record that does not exist returns `404`. A record that belongs to another owner returns `403 FORBIDDEN`, except where the known gap in [section 8](#8-known-gaps) applies.
- **Referenced records:** when creating a batch, a product or supplier that is missing or belongs to another owner returns the same response, `400 INVALID_REFERENCE`. This stops a caller from discovering which IDs exist.

## 4. Error code catalogue

| Code | HTTP status | When it is used |
| :--- | :--- | :--- |
| `INVALID_INPUT` | 400 | Body, query or path fails validation (missing field, wrong type, out of range, malformed ID) |
| `INVALID_REFERENCE` | 400 | A referenced product or supplier does not exist, or is not yours |
| `INVALID_CREDENTIALS` | 401 | Login email or password is wrong (same message for both) |
| `UNAUTHORIZED` | 401 | No token, bad token, expired token, or user no longer exists |
| `FORBIDDEN` | 403 | Logged in, but the record belongs to another owner |
| `NOT_FOUND` | 404 | Unknown route |
| `PRODUCT_NOT_FOUND` | 404 | Product ID does not exist |
| `SUPPLIER_NOT_FOUND` | 404 | Supplier ID does not exist |
| `BATCH_NOT_FOUND` | 404 | Batch ID does not exist |
| `METHOD_NOT_ALLOWED` | 405 | Wrong HTTP method for the route |
| `EMAIL_TAKEN` | 409 | Signup with an email that is already registered |
| `DUPLICATE_BATCH` | 409 | Same batch number used twice for one supplier |
| `SUPPLIER_HAS_BATCHES` | 409 | Supplier delete refused because batches refer to it |
| `PRODUCT_HAS_BATCHES` | 409 | Product delete refused because batches refer to it (**known gap**, see section 8) |
| `INSUFFICIENT_STOCK` | 409 | Adjustment would make `quantity_remaining` negative |
| `INTERNAL_ERROR` | 500 | Unexpected failure. Generic message only. |

**400 versus 409:** `400` means the request itself is malformed or refers to something invalid. `409` means the request is well formed but conflicts with the current state (for example, a duplicate, a record that still has children, or insufficient stock).

## 5. Resources

### User

| Field | Type | Notes |
| :--- | :--- | :--- |
| `id` | integer | Read-only |
| `email` | string | Unique, stored lowercase, up to 255 characters |
| `role` | string | Always `owner` in Week 2 |
| `created_at` | timestamp | Read-only |

### Product

| Field | Type | Required | Rules |
| :--- | :--- | :--- | :--- |
| `id` | integer | Read-only | |
| `owner_id` | integer | Read-only | Set from the token |
| `name` | string | Yes | 1 to 150 characters, trimmed; blank is rejected |
| `generic_name` | string | No | Up to 150 characters |
| `category` | string | Yes | 1 to 80 characters |
| `unit` | string | Yes | 1 to 30 characters, for example `tablet` |
| `reorder_level` | integer | No (default 0) | Zero or greater |
| `created_at` | timestamp | Read-only | |

### Supplier

| Field | Type | Required | Rules |
| :--- | :--- | :--- | :--- |
| `id` | integer | Read-only | |
| `owner_id` | integer | Read-only | Set from the token |
| `name` | string | Yes | 1 to 150 characters, trimmed |
| `phone` | string | No | Up to 30 characters, stored as text so leading zeros and `+234` are kept |
| `email` | string | No | Valid email, up to 254 characters |
| `created_at` | timestamp | Read-only | |

### Batch

A batch is one delivery of one product from one supplier, with its own expiry date.

| Field | Type | Required | Rules |
| :--- | :--- | :--- | :--- |
| `id` | integer | Read-only | |
| `product_id` | integer | Yes | Must be one of your products |
| `supplier_id` | integer | Yes | Must be one of your suppliers |
| `batch_number` | string | Yes | 1 to 60 characters, trimmed; unique per supplier |
| `quantity_received` | integer | Yes | Greater than zero |
| `quantity_remaining` | integer | Read-only | Set to `quantity_received` on create. Changed only by adjustments. Never negative. |
| `expiry_date` | date | Yes | Must be later than `received_date` |
| `received_date` | date | Yes | |

### Stock adjustment

| Field | Type | Required | Rules |
| :--- | :--- | :--- | :--- |
| `id` | integer | Read-only | |
| `batch_id` | integer | Read-only | Set from the path |
| `quantity_change` | integer | Yes | Non-zero. Negative for `sold`, `damaged` and `expired`. May be positive or negative for `correction`. |
| `reason` | string | Yes | One of `sold`, `damaged`, `expired`, `correction` |
| `note` | string | No | Up to 255 characters |
| `created_at` | timestamp | Read-only | |

## 6. Endpoints

Every endpoint below requires a token unless marked otherwise.

### Health

| Method | Path | Auth | Success | Notes |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/health` | No | `200` | Returns `{"status": "ok"}` |

### Products

| Method | Path | Success | Errors | Notes |
| :--- | :--- | :--- | :--- | :--- |
| POST | `/products` | `201` | `400`, `401` | Owner is set from the token |
| GET | `/products` | `200` | `401` | Returns your products only (empty list if none) |
| GET | `/products/{product_id}` | `200` | `400`, `401`, `403`, `404` | |
| PUT | `/products/{product_id}` | `200` | `400`, `401`, `403`, `404` | Full update. `name`, `category`, `unit` are required. `generic_name` cannot be cleared to null by omitting it (**known gap**). |
| DELETE | `/products/{product_id}` | `204` | `400`, `401`, `403`, `404`, `409` | Intended: `409 PRODUCT_HAS_BATCHES` if batches exist (**known gap**, currently `500`) |

Clients cannot set `id`, `owner_id` or `created_at`.

### Suppliers

| Method | Path | Success | Errors | Notes |
| :--- | :--- | :--- | :--- | :--- |
| POST | `/suppliers` | `201` | `400`, `401` | |
| GET | `/suppliers` | `200` | `401` | Your suppliers only |
| GET | `/suppliers/{supplier_id}` | `200` | `400`, `401`, `403`, `404` | |
| PUT | `/suppliers/{supplier_id}` | `200` | `400`, `401`, `403`, `404` | |
| DELETE | `/suppliers/{supplier_id}` | `204` | `400`, `401`, `403`, `404`, `409` | `409 SUPPLIER_HAS_BATCHES` if any batch refers to the supplier |

### Batches

| Method | Path | Success | Errors | Notes |
| :--- | :--- | :--- | :--- | :--- |
| POST | `/batches` | `201` | `400`, `401`, `409` | Checks: product and supplier exist and are yours (`400 INVALID_REFERENCE`); batch number unique per supplier (`409 DUPLICATE_BATCH`); expiry after received date (`400`). |
| GET | `/batches` | `200` | `401` | Batches of your products only |
| GET | `/batches/expiring-soon?days=N` | `200` | `400`, `401` | See [section 7.3](#73-expiring-soon). `days` defaults to 30. |
| GET | `/batches/{batch_id}` | `200` | `400`, `401`, `404` | Another owner's batch returns `404` (**known gap**: intended `403`) |

Declaration order matters in the router: `/batches/expiring-soon` is declared before `/batches/{batch_id}`, so the query is not read as a batch ID.

### Stock adjustments

| Method | Path | Success | Errors | Notes |
| :--- | :--- | :--- | :--- | :--- |
| POST | `/batches/{batch_id}/adjustments` | `201` | `400`, `401`, `403`, `404`, `409` | Atomic, row-locked. See [section 7.2](#72-stock-adjustments). |
| GET | `/batches/{batch_id}/adjustments` | `200` | `400`, `401`, `403`, `404` | History ordered by `created_at`, oldest first |

**Request body for `POST /batches/{batch_id}/adjustments`:**

```json
{ "quantity_change": -5, "reason": "sold", "note": "Morning sale" }
```

**Success response (`201`):**

```json
{
  "id": 1,
  "batch_id": 1,
  "quantity_change": -5,
  "reason": "sold",
  "note": "Morning sale",
  "created_at": "2026-10-21T09:12:44Z"
}
```

## 7. Business rules

### 7.1 Batch receipt

- `quantity_received` must be greater than zero.
- `quantity_remaining` is set by the server to `quantity_received`. The client cannot set it.
- `expiry_date` must be later than `received_date`. A batch whose expiry is on or before its received date is rejected with `400`.
- `batch_number` is unique per supplier, enforced by a database unique index on `(supplier_id, batch_number)` as well as the application check.

### 7.2 Stock adjustments

- The only way to change `quantity_remaining` is to create an adjustment.
- `sold`, `damaged` and `expired` must have a negative `quantity_change`. `correction` may be positive or negative. A zero change is rejected with `400`.
- The steps run in one database transaction, with the batch row locked (`SELECT ... FOR UPDATE`) so two requests cannot both read the same balance:
  1. Lock the batch and check that it exists (`404`) and that its product belongs to you (`403`).
  2. Calculate the new balance. If it would be negative, roll back and return `409 INSUFFICIENT_STOCK`. The balance is unchanged.
  3. Insert the adjustment and update the balance, then commit.
- The database also has a check constraint `quantity_remaining >= 0` as a second safety net.
- The history endpoint lets you verify that `quantity_received` plus the sum of all adjustments equals `quantity_remaining`.

### 7.3 Expiring soon

`GET /batches/expiring-soon?days=N` returns batches of your products that:

- have `quantity_remaining > 0` (zero-stock batches are excluded because nothing is at risk),
- have `expiry_date` from today through today plus N days, **inclusive at both ends**, and
- are not already expired (expired batches are not included).

Rules for this query:

- "Today" is the server's local date. If the server runs in UTC, that is one hour behind Lagos time (UTC+1) for the hour after midnight in Lagos.
- `days` must be a whole number. Anything else returns `400 INVALID_INPUT`.
- The default is 30. The intended range is 0 to 365 (**known gap**: the current code has no upper limit).

Expired batches are not listed by a separate endpoint in Week 2.

### 7.4 Deletion

- Deleting a product or supplier that still has batches is refused with `409`. Stock history is never cascade-deleted.
- A supplier delete returns `409 SUPPLIER_HAS_BATCHES`. A product delete should return `409 PRODUCT_HAS_BATCHES` (**known gap**).

### 7.5 Input handling

- Unknown fields in a request body are ignored.
- Strings are trimmed of leading and trailing spaces before validation. A name made only of spaces is rejected.
- Every text field has a maximum length. Longer input returns `400`.
- A path ID that is not a whole number, such as `/products/abc`, returns `400 INVALID_INPUT`.
- A request body sent with the wrong content type returns `400`, not a stack trace.

## 8. Not yet implemented

These are part of the Week 2 plan but are not built yet:

- `GET /products/{product_id}/batches`
- `GET /suppliers/{supplier_id}/batches`
- A list of expired batches (`GET /batches?status=expired` or `GET /batches/expired`)

Week 3 work (automated test suite, rate limiting, pagination, deployment) is out of scope for this document.
