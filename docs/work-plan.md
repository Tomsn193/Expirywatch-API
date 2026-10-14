# ExpiryWatch API — Three-Week Work Plan

## Week 1 — Design and core products API
- Finish the idea one-pager, repository, README, and environment example.
- Design the entities and relationships; create the ERD and API specification.
- Build and migrate the products table.
- Implement product create/list/retrieve/update/delete operations.
- Add dummy records, sample requests, and basic verification evidence.
- Prepare and give the five-minute mentor presentation.

## Week 2 — Authentication and robustness
- Review and respond to Week 1 feedback.
- Add authentication and password hashing.
- Add suppliers, batches, stock adjustments, and relationships.
- Implement the expiring-soon query and ownership checks.
- Standardise validation and error handling.
- Maintain the issue log and tag the week-2 version.

## Week 3 — Quality and delivery
- Add unit and integration tests.
- Complete API docs, setup guide, and security/performance notes.
- Add pagination and indexes where needed.
- Deploy the API or verify the clean-machine run guide.
- Record the walkthrough, reflection, and declaration.
- Tag the week-3 version and submit the final package.

## Top risks and mitigations
1. Stock consistency: make the batch balance change through recorded adjustments, not arbitrary edits.
2. Migrations: use Alembic from the beginning and commit each migration.
3. Delivery/deployment: keep local setup reliable and test deployment before the final day.