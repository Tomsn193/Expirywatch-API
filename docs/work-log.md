## 2026-10-19 — Session: Week 2 Preparation
- Goal: Update data model for Auth and Ownership.
- Completed: Added `users` table to DBML and Markdown docs. Added `owner_id` to `products` and resolved field lengths.
- Decisions made: To handle existing Week 1 products with no owner, I will use a backfill strategy in the upcoming Alembic migration: add the column as nullable, create a dummy user, assign the products, and then make the column `NOT NULL`.
- Next action: Build the SQLAlchemy `User` model and generate the migration.