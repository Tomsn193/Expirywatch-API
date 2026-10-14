# ExpiryWatch API

A learning project focused on building a FastAPI backend for tracking product records, with future support for stock batches and expiry-date monitoring.

## Overview

ExpiryWatch is designed for owners of small pharmacies and patent medicine shops in Nigeria. The project addresses a common operational issue: products and stock items are often tracked informally, which can lead to expired items going unnoticed, causing financial waste and potential safety risks.

The system aims to provide a simple, reliable way to manage product information and, later, monitor stock movement, batch details, and expiry dates with minimal friction.

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (running locally via Docker)

## Current Status

Week 1 — product CRUD is in progress.

## Features

- Product creation, reading, updating, and deletion
- Local PostgreSQL setup for development
- Clean API structure using FastAPI and SQLAlchemy
- Future support for inventory batches, expiry tracking, and stock alerts

## Prerequisites

Before you begin, make sure you have:

- Python 3.10 or newer
- Docker installed and running

## Local Setup

1. Clone the repository and move into the project directory.
2. Copy `.env.example` to a new file named `.env`.
3. Set a strong local password for `POSTGRES_PASSWORD` and use the same value in `DATABASE_URL`.
4. Start the database container:

   ```bash
   docker compose up -d
   ```

5. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

6. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

7. Run the application (when the project is ready):

   ```bash
   uvicorn app.main:app --reload
   ```

8. Database migrations and additional run commands will be added as the project evolves.

## Environment and Security Notes

- The local PostgreSQL database is bound to `127.0.0.1` and is intended only for development.
- Keep your `.env` file private.
- In production, store credentials using your deployment platform's secret manager and keep the database on a private network rather than exposing local development settings.

## Documentation

See the `/docs` folder for the project concept, work plan, data model, and API specifications.

## Entity Relationship Diagram (ERD)

![ExpiryWatch ERD](docs/erd.png)

## Warning

This is a learning project. Use dummy data only. Never input real pharmacy stock records, personal customer details, or real passwords.
