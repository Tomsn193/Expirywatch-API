# Issue Log — ExpiryWatch API

## ISSUE-001 — Pydantic EmailValidator Rejects .test TLD
- Date discovered: 2026-10-20
- Status: Resolved
- Type: Validation
- Expected behaviour: The API should accept `contact@lagospharma.test` as a valid dummy email.
- Actual behaviour: Pydantic returned `400 INVALID_INPUT` stating the part after the @-sign is a special-use or reserved name.
- Fix or next action: Used `.com` for dummy data to maintain strict validation rules.

## ISSUE-002 — ModuleNotFoundError for email_validator
- Date discovered: 2026-10-20
- Status: Resolved
- Type: Setup blocker
- Expected behaviour: The FastAPI server should start successfully after adding `EmailStr`.
- Actual behaviour: Server crashed on startup with `ImportError: email-validator is not installed`.
- Fix or next action: Ran `pip install email-validator` and added it to `requirements.txt`.

## ISSUE-003 — SQLAlchemy Mapper KeyError for StockAdjustment
- Date discovered: 2026-10-20
- Status: Resolved
- Type: Setup blocker
- Actual behaviour: Server threw `KeyError: 'StockAdjustment'` during startup.
- Root cause: SQLAlchemy tries to map all relationships on startup but couldn't find the `StockAdjustment` class in the registry.
- Fix or next action: Built the `app/models/adjustment.py` file and imported it into `app/models/__init__.py`.

## ISSUE-004 — Deleting a Product with Batches Returns 500 Error
- Date discovered: 2026-10-21
- Status: Resolved
- Type: Bug / Data integrity
- Actual behaviour: The database threw an Integrity Error (Foreign Key violation), resulting in an unhandled 500 Internal Server Error.
- Fix or next action: Added `if db_product.batches: raise APIError(409, ...)` in the delete route.

## ISSUE-005 — Login Rejects Short Passwords with 400 Bad Request
- Date discovered: 2026-10-21
- Status: Resolved
- Type: Bug
- Actual behaviour: Returned `400 Bad Request` instead of `401 Unauthorized` for a short incorrect password.
- Root cause: Reusing `UserCreate` (which enforces min-length for signups) for the login payload.
- Fix or next action: Created a dedicated `UserLogin` schema without length validation constraints.

## ISSUE-006 — Seed Script Fails on owner_id NOT NULL Constraint
- Date discovered: 2026-10-21
- Status: Resolved
- Type: Bug
- Root cause: Week 2 introduced mandatory ownership (`owner_id`) to products, breaking the Week 1 seed script.
- Fix or next action: Updated the script to accept a user email via CLI argument and dynamically apply their `id`.

## ISSUE-007 — Pytest Rate Limit Blocking
- Date discovered: 2026-10-28
- Status: Resolved
- Type: Testing / Configuration
- Expected behaviour: The test suite runs all 9 tests successfully.
- Actual behaviour: `test_cross_owner_forbidden` failed with `KeyError: 'access_token'`. The logs showed `429 Too Many Requests`.
- Root cause: Rapid successive calls to `/auth/login` triggered the newly implemented `slowapi` rate limiter during test setup.
- Fix or next action: Extracted the limiter instance into a shared `app/limiter.py` module and explicitly set `limiter.enabled = False` in `tests/conftest.py`.

## ISSUE-008 — Custom Exception Handler Missing Attribute
- Date discovered: 2026-10-28
- Status: Resolved
- Type: Bug
- Actual behaviour: Tests triggered an `AttributeError: 'APIError' object has no attribute 'error_code'` when trying to return a 409 or 401 JSON response.
- Root cause: Mismatch between the variable name used in the global `api_error_handler` and the attributes defined in the custom `APIError` class.
- Fix or next action: Updated `app/main.py` exception handler to utilize `getattr(exc, "code", getattr(exc, "error_code", "INTERNAL_ERROR"))` to safely parse the correct attribute.