# ExpiryWatch API

- Track: Backend Development
- Stack: Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL
- Target user: Owner of a small pharmacy or patent medicine shop in Nigeria
- Problem: Stock can expire unnoticed when quantities and expiry dates are tracked informally. This can cause avoidable waste and a potential safety risk.
- Entities: products, suppliers, batches, stock_adjustments
- Core flow: add a product -> receive a batch with an expiry date -> list batches expiring within N days -> record a stock adjustment

## In scope
- Create, list, retrieve, update, and delete product records
- Plan the schema for products, suppliers, batches, and stock adjustments
- In later weeks, record batches, expiry dates, and stock adjustments
- In later weeks, filter batches that expire within a requested number of days
- Dummy data only

## Out of scope
- Payments or a point-of-sale system
- Barcode scanning and file/image uploads
- SMS/email notifications
- Multi-branch pharmacy management
- Real pharmacy or customer data

## Top 3 risks
1. Stock quantities may become inconsistent if adjustments are not modelled carefully.
2. Learning database migrations may take longer than expected.
3. Deployment may take longer than expected, so the run guide must be kept working throughout.