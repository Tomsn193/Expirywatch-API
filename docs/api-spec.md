# ExpiryWatch API Specification

## Common API Conventions
*   **Base URL (Local):** `http://127.0.0.1:8000`
*   **Format:** JSON request and response bodies.
*   **Status Codes:** 
    *   `201 Created` for successful creation.
    *   `200 OK` for successful retrieval or update.
    *   `204 No Content` for successful deletion.
    *   `400 Bad Request` for invalid inputs (overriding FastAPI's default 422).
    *   `404 Not Found` when an ID does not exist.
*   **Error Format:**
    ```json
    {
      "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable description"
      }
    }
    ```
    Validation errors (`400`, code `INVALID_INPUT`) also include a `details` list:
    ```json
    {
      "error": {
        "code": "INVALID_INPUT",
        "message": "Validation failed",
        "details": [{ "field": "reorder_level", "message": "Input should be greater than or equal to 0" }]
      }
    }
    ```
    Unknown routes return `404 NOT_FOUND`, wrong methods return `405 METHOD_NOT_ALLOWED`, and unexpected server errors return `500 INTERNAL_ERROR` with no internal details.

## Week 1: Product Endpoints (Implemented)

| Method | Path | Purpose | Expected Success | Expected Error |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/products` | Create a product | `201 Created` | `400 Bad Request` (invalid fields) |
| **GET** | `/products` | List all products | `200 OK` | `200 OK` (empty list if none) |
| **GET** | `/products/{id}` | Retrieve one product | `200 OK` | `404 Not Found` |
| **PUT** | `/products/{id}` | Full update of editable fields | `200 OK` | `400 Bad Request`, `404 Not Found` |
| **DELETE** | `/products/{id}` | Delete a product | `204 No Content` | `404 Not Found` |
| **GET** | `/health` | Check the API is running (returns `{"status": "ok"}`) | `200 OK` | n/a |

*Note: For PUT requests, `name`, `category`, `unit`, and `reorder_level` are required. `generic_name` is optional. Clients cannot update the `id` or `created_at` fields.*

## Week 2: Planned Endpoints

| Method | Path | Purpose | Phase |
| :--- | :--- | :--- | :--- |
| **POST** | `/suppliers` | Create a supplier | Week 2 |
| **GET** | `/suppliers` | List suppliers | Week 2 |
| **GET** | `/suppliers/{id}` | Retrieve one supplier | Week 2 |
| **POST** | `/batches` | Record a batch | Week 2 |
| **GET** | `/batches/expiring-soon?days=30` | List batches expiring within N days | Week 2 |
| **POST** | `/batches/{id}/adjustments` | Record a stock adjustment | Week 2 |