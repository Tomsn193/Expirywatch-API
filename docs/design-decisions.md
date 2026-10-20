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

## DEC-007 — Field Length Reconciliations
- Context: ERD and Data Model docs had mismatched lengths in Week 1.
- Decision: Settled on `email` as String(254), `batch_number` as String(60), and `note` as String(255).
- Reason: 254 is standard for emails, 60 is plenty for dummy batch numbers, and 255 keeps notes concise.

## DEC-008 — Ownership Hierarchy
- Context: Need to verify ownership for batches and stock adjustments.
- Decision: Add `owner_id` only to `products` and `suppliers`.
- Reason: A batch belongs to a product, and an adjustment belongs to a batch. Ownership can be checked securely through the chain without duplicating `owner_id` on every table.

## DEC-009 — Open Questions Resolution
- Context: Two open questions from Week 1 needed answers.
- Decision: 
  1. `name` and `unit` together will NOT be enforced as strictly unique at the database level for now.
  2. `expiry_date` MUST be later than `received_date`.
- Reason: Rejecting past expiry dates prevents bad data entry.