# ExpiryWatch API
A learning project: a FastAPI backend for tracking product records and, in later stages, stock batches and expiry dates.

**Target User & Problem:** Designed for owners of small pharmacies or patent medicine shops in Nigeria. It solves the problem of stock expiring unnoticed when quantities and expiry dates are tracked informally, which causes avoidable waste and potential safety risks.

**Stack:** Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL (via Docker).

**Current Status:** Week 1 — product CRUD in progress.

**Prerequisites:** 
* Python 3.10+
* Docker (for the local PostgreSQL database)

**Setup and Run Instructions:**
1. Clone the repository and navigate into the project directory.
2. Copy `.env.example` to a new file named `.env` and update any local credentials if necessary.
3. Start the local database using Docker:
   `docker compose up -d`
4. Create and activate your virtual environment:
   `python -m venv .venv`
   `source .venv/bin/activate` (Mac/Linux) or `.\.venv\Scripts\Activate.ps1` (Windows)
5. Install dependencies:
   `pip install -r requirements.txt`
6. (Database migrations and run commands will be added here once implemented).

**Documentation:**
See the `/docs` folder for the idea one-pager, work plan, data model, and API specifications.

**Warning:** 
This is a learning project. Use dummy data only. Never input real pharmacy stock records, personal customer details, or real passwords.