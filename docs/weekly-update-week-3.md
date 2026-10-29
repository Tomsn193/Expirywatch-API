# Week 3 Technical Reflection & Test Results

## 1. Addressing Peer Review Feedback
The Week 1 peer review highlighted strong domain understanding, data modeling, and validation structures. The primary areas identified for improvement were:
1.  **Add automated tests to strengthen reliability.**
2.  **Document a stronger review and issue-tracking workflow.**

**Resolution in Week 3:**
*   **Testing:** Implemented a robust `pytest` suite utilizing an isolated, in-memory SQLite database. The suite specifically targets critical failure points (401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict) and covers the complex atomic locking logic in the inventory adjustment route.
*   **Tracking:** Expanded the formal `issue-log.md` (see docs) to track environment, validation, and configuration blockers encountered during development, providing a clear audit trail of bug resolution.

## 2. Week 3 Test Results
The final integration test suite executes 9 comprehensive checks across the authentication, product CRUD, and inventory systems.

*   **Test Environment:** `pytest`, `httpx`, `anyio`
*   **Database:** `sqlite:///:memory:` (Ephemeral override via `conftest.py`)
*   **Execution Time:** ~4.79 seconds
*   **Pass Rate:** 100% (9/9 passed)

**Key Test Coverage:**
*   `test_auth.py`: Validates signup success, duplicate email blocking (409), login success, and invalid credential rejection (401).
*   `test_products.py`: Validates protected route enforcement (401), successful record creation, not-found handling (404), and strict cross-owner resource blocking (403).
*   `test_inventory.py`: Validates that the database row-locking mechanism correctly rejects adjustments that would drive `quantity_remaining` below zero (409).

## 3. Architecture, Security, & Performance Enhancements
During Week 3, the codebase was shifted from purely functional to production-ready:
*   **Global Pagination:** Implemented `skip` and `limit` query parameters on all list endpoints (e.g., `GET /products`) to ensure consistent response times regardless of database scale.
*   **Rate Limiting:** Integrated `slowapi` to restrict the `/auth/login` endpoint to 5 requests per minute, mitigating brute-force and dictionary attacks.
*   **CORS Configuration:** Replaced open local access with explicitly defined `allow_origins` headers via `CORSMiddleware`.
*   **Code Quality:** Refactored deprecated Pydantic V1 `class Config:` blocks to modern V2 `ConfigDict` implementations, resolving terminal warnings.

## 4. Remaining Risks & Future Roadmap
While the backend is structurally sound, scaling considerations remain:
1.  **Expiring-Soon Query Scalability:** As the batches table grows, the query checking `expiry_date` offsets could become a bottleneck. Indexing the `expiry_date` column will be necessary in future iterations.
2.  **Background Processing:** Currently, users must actively poll the expiring-soon endpoint. Implementing a task queue (like Celery or RQ) with a cron job to automatically email owners about pending expirations would significantly improve the product's proactive utility.