# Week 2 — Oduone Oritsegbubemi — Backend — ExpiryWatch API

## Delivered
- 2.1 Auth and authorisation: Added JWT authentication, password hashing, and protected endpoints.
- 2.2 Relationships, validation, errors: Implemented Suppliers, Batches, and Stock Adjustments with atomic transactions.

## Changed After Feedback
- No mentor feedback received for Week 1 at the time of writing.

## Key Technical Decisions
- DEC-007: Used JWT bearer tokens for stateless authentication.
- DEC-008: Added `owner_id` to Products and Suppliers; Batches and Adjustments verify ownership through their parent records.
- DEC-010: Stock changes are handled exclusively via an adjustments table using `with_for_update()` row-locking to prevent race conditions.

## Blockers / Risks
- Migration on existing rows required a backfill strategy to satisfy `NOT NULL` constraints.
- Strict Pydantic email validation rejected `.test` dummy domains, requiring use of `.com`.

## AI and Sources Used
- Utilized Gemini as a thought partner to structure the Alembic backfill migration and configure the FastAPI dependency injection for the `get_current_user` auth flow.