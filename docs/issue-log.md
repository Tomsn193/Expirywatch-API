# Issue Log — ExpiryWatch API

## ISSUE-001 — Pydantic EmailValidator Rejects .test TLD
- Date discovered: 2026-10-20
- Status: Resolved
- Type: Validation
- Expected behaviour: The API should accept `contact@lagospharma.test` as a valid dummy email.
- Actual behaviour: Pydantic returned `400 INVALID_INPUT` stating the part after the @-sign is a special-use or reserved name.
- Steps to reproduce: Send a POST request to `/suppliers` with `contact@lagospharma.test`.
- Root cause: `email-validator` strictly enforces valid global TLDs by default.
- Options considered: Disable DNS/TLD validation in the schema, or simply use a standard `.com` domain for dummy data.
- Fix or next action: Used `.com` for dummy data to maintain strict validation rules.
- How the fix was verified: Resent the request with `contact@lagospharma.com` and received `201 Created`.
- Related commit: "fix: resolve auth, validation, and ownership edge cases from review"

## ISSUE-002 — ModuleNotFoundError for email_validator
- Date discovered: 2026-10-20
- Status: Resolved
- Type: Setup blocker
- Expected behaviour: The FastAPI server should start successfully after adding `EmailStr` to the Supplier schema.
- Actual behaviour: Server crashed on startup with `ImportError: email-validator is not installed, run pip install 'pydantic[email]'`.
- Steps to reproduce: Add `EmailStr` to a Pydantic schema and run `uvicorn app.main:app --reload` without the validator installed.
- Root cause: Pydantic V2 requires an optional dependency to process `EmailStr`.
- Options considered: Revert to standard string validation with Regex, or install the required package.
- Fix or next action: Ran `pip install email-validator` and added it to `requirements.txt`.
- How the fix was verified: Restarted the Uvicorn server successfully.
- Related commit: "fix: resolve auth, validation, and ownership edge cases from review"

## ISSUE-003 — SQLAlchemy Mapper KeyError for StockAdjustment
- Date discovered: 2026-10-20
- Status: Resolved
- Type: Setup blocker
- Expected behaviour: Server starts and Alembic generates the migration for Batches and Suppliers.
- Actual behaviour: Server threw `KeyError: 'StockAdjustment'` and `sqlalchemy.exc.InvalidRequestError` during startup.
- Steps to reproduce: Define a `relationship("StockAdjustment")` in the `Batch` model before the `StockAdjustment` model actually exists in the code.
- Root cause: SQLAlchemy tries to map all relationships on startup but couldn't find the `StockAdjustment` class in the registry.
- Options considered: Comment out the relationship temporarily, or build the StockAdjustment model immediately.
- Fix or next action: Built the `app/models/adjustment.py` file and imported it into `app/models/__init__.py`.
- How the fix was verified: Server booted cleanly and `alembic revision --autogenerate` succeeded.
- Related commit: "feat: add stock adjustments table"

## ISSUE-004 — Deleting a Product with Batches Returns 500 Error
- Date discovered: 2026-10-21
- Status: Resolved
- Type: Bug / Data integrity
- Expected behaviour: Attempting to delete a product that has associated batches should be safely blocked with a 409 Conflict.
- Actual behaviour: The database threw an Integrity Error (Foreign Key violation), resulting in an unhandled 500 Internal Server Error sent to the client.
- Steps to reproduce: Create a product, create a batch for that product, then send `DELETE /products/{id}`.
- Root cause: Missing application-level check for child records before issuing the delete command.
- Options considered: Configure cascading deletes at the DB level, or catch the exception. Decided to explicitly check for `.batches` to prevent accidental history loss.
- Fix or next action: Added `if db_product.batches: raise APIError(409, "PRODUCT_HAS_BATCHES", ...)` in the delete route.
- How the fix was verified: Sent the DELETE request to Product 1 and successfully received the custom 409 JSON error.
- Related commit: "fix: resolve auth, validation, and ownership edge cases from review"

## ISSUE-005 — Login Rejects Short Passwords with 400 Bad Request
- Date discovered: 2026-10-21
- Status: Resolved
- Type: Bug
- Expected behaviour: Typing a wrong, short password (e.g., "pass") during login should return `401 Unauthorized (INVALID_CREDENTIALS)`.
- Actual behaviour: Returned `400 Bad Request (INVALID_INPUT)` because it failed Pydantic's 8-character minimum length validation.
- Steps to reproduce: Send `POST /auth/login` with `"password": "pass"`.
- Root cause: The `/login` route was reusing the `UserCreate` schema, which strictly enforces password creation rules (min length 8).
- Options considered: Remove length validation from UserCreate, or split the schemas.
- Fix or next action: Created a dedicated `UserLogin` schema in `app/schemas/user.py` that just takes standard strings without length limits.
- How the fix was verified: Attempted login with "pass" and received the correct 401 response.
- Related commit: "fix: resolve auth, validation, and ownership edge cases from review"

## ISSUE-006 — Seed Script Fails on owner_id NOT NULL Constraint
- Date discovered: 2026-10-21
- Status: Resolved
- Type: Bug
- Expected behaviour: `python scripts/seed_products.py` inserts dummy products.
- Actual behaviour: SQLAlchemy threw an IntegrityError because `owner_id` was missing.
- Steps to reproduce: Run the Week 1 seed script after applying the Week 2 database migrations.
- Root cause: Week 2 introduced mandatory ownership (`owner_id` integer) to the `products` table, but the seed script wasn't updated to provide one.
- Options considered: Hardcode an ID of `1`, or dynamically look up a user.
- Fix or next action: Updated the script to accept a user email via CLI argument (`sys.argv`), lookup the user, and apply their `id` to the dummy records.
- How the fix was verified: Ran `python scripts/seed_products.py owner1@example.com` and confirmed products were created and visible in `GET /products`.
- Related commit: "chore: update sample requests with dynamic testing IDs"