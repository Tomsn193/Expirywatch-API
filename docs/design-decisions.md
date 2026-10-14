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