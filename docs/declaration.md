# Declaration of Originality and Material Use

**Project Name:** ExpiryWatch API  
**Developer:** Oritsegbubemi Oduone  
**Track:** Backend Development (BuildLab Stage 1)  
**Date:** October 2026  

---

## 1. Originality Statement
I hereby declare that the codebase, database design, API specification, and documentation submitted for the ExpiryWatch API project are my own original work, except where explicitly credited below.

## 2. External Libraries & Frameworks Used
*   **Web Framework:** FastAPI, Starlette, Uvicorn
*   **Database & ORM:** PostgreSQL, SQLAlchemy 2.0, Alembic, Driver (`psycopg2-binary`)
*   **Data Validation:** Pydantic V2, `email-validator`
*   **Authentication & Security:** PyJWT, Passlib (Bcrypt), SlowAPI (Rate Limiting)
*   **Testing Infrastructure:** Pytest, HTTPX, AnyIO, SQLite (In-Memory)

## 3. Material AI Assistance Declaration
In accordance with BuildLab submission guidelines, I disclose the following AI assistance during the project:
*   **Tool Used:** Gemini, Claude
*   **Scope of Assistance:**
    *   Architectural refinement for atomic row-locking patterns (`with_for_update()`).
    *   Debugging pytest setup issues involving `slowapi` rate-limiter interactions in test environments.
    *   Structuring comprehensive Markdown documentation (`architecture.md`, `issue-log.md`, and technical reflections).
*   **Verification:** All AI-suggested code snippets, schema constraints, and test fixtures were manually implemented, customized, and verified against local PostgreSQL and SQLite test environments.