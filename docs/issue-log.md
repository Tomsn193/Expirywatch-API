# ExpiryWatch API — Issue Log

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
- How verified: Resent the request with `contact@lagospharma.com` and received `201 Created`.