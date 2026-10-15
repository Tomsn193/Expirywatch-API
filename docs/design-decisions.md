# Design Decisions

## DEC-001 — PostgreSQL for the database
*   **Context:** The project stores products, suppliers, batches, and adjustments with relationships.
*   **Decision:** Use PostgreSQL via Docker for local development.
*   **Alternatives considered:** SQLite or a document database.
*   **Reason:** Relational constraints and foreign keys fit the planned data model securely.

## DEC-002 — Expiry date belongs to batches
*   **Context:** One product may arrive in multiple batches with different expiry dates.
*   **Decision:** Store `expiry_date` on `batches`, not `products`.
*   **Reason:** Expiry belongs to a particular physical delivery, not the abstract product definition.

## DEC-003 — Week 1 implementation scope
*   **Context:** The project must be completed over three weeks.
*   **Decision:** Implement only the `products` endpoints in Week 1.
*   **Reason:** Proves the core data/API workflow without expanding the first milestone too far.

## DEC-004 — Invalid-input status code
*   **Context:** FastAPI defaults to 422 for request validation; the BuildLab guide mentions 400 for bad input.
*   **Decision:** Override FastAPI's default and return `400 Bad Request` for validation failures.
*   **Reason:** Aligns exactly with the assessment expectations and the API specification.

## DEC-005 — One consistent error format
*   **Context:** FastAPI returns different shapes by default (`{"detail": ...}` for HTTP errors, a list for validation errors), and unhandled exceptions can leak internals.
*   **Decision:** All errors go through handlers in `app/errors.py` and return `{"error": {"code", "message", "details"?}}`. A catch-all handler returns a generic 500 and logs the real error server-side only.
*   **Reason:** Clients can parse every error the same way, and no stack traces or internals are exposed.

## DEC-006 — No credentials in code
*   **Context:** Database credentials must never be committed to a public repository.
*   **Decision:** `DATABASE_URL` is read only from the environment (`.env` locally). The app and Alembic fail with a clear message if it is missing. `.env.example` holds placeholders only.
*   **Reason:** Prevents secrets from leaking through the code or git history.

