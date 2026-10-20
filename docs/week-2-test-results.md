# ExpiryWatch API — Week 2 Test Results

**Date:** 2026-10-20  
**Environment:** Local Development (`http://127.0.0.1:8000`)  
**Database:** PostgreSQL (Docker container)  

---

## 1. Carry-Over & Baseline Verification (Week 1)

| Check | Target Route | Expected Result | Actual Result / Response | Status |
| :--- | :--- | :--- | :--- | :--- |
| Create valid product | `POST /products` | 201 Created | `201 Created` (ID generated, `owner_id` set) | Pass |
| List products | `GET /products` | 200 OK | `200 OK` (Returned active product list) | Pass |
| Retrieve existing product | `GET /products/1` | 200 OK | `200 OK` (Returned Product ID 1) | Pass |
| Retrieve non-existent ID | `GET /products/9999` | 404 Not Found | `404 Not Found` (`PRODUCT_NOT_FOUND`) | Pass |
| Update product details | `PUT /products/1` | 200 OK | `200 OK` (Updated name returned) | Pass |
| Missing required fields | `POST /products` | 400 Bad Request | `400 Bad Request` (`INVALID_INPUT`) | Pass |
| Negative reorder level | `POST /products` | 400 Bad Request | `400 Bad Request` (`INVALID_INPUT`) | Pass |
| Blank name string | `POST /products` | 400 Bad Request | `400 Bad Request` (`INVALID_INPUT`) | Pass |
| Delete existing product | `DELETE /products/1` | 204 No Content | `204 No Content` (Empty response body) | Pass |
| Seed data visibility | `GET /products` | 200 OK | `200 OK` (Seed products listed) | Pass |

---

## 2. Authentication & Authorization Verification (Task 2.1)

| Check | Target Route | Expected Result | Actual Result / HTTP Response Summary | Status |
| :--- | :--- | :--- | :--- | :--- |
| **User Registration** | `POST /auth/signup` | 201 Created | `201 Created` (Returned ID 2, `email: owner1@example.test`, no hash leaked) | Pass |
| **User Login** | `POST /auth/login` | 200 OK | `200 OK` (Returned `access_token` JWT string) | Pass |
| **Get Logged-in Profile** | `GET /auth/me` | 200 OK | `200 OK` (Decoded sub claim `2`, returned `owner1` profile) | Pass |
| **Create Product (Auth)** | `POST /products` | 201 Created | `201 Created` (Assigned `owner_id: 2` automatically) | Pass |
| **Create Product (No Token)** | `POST /products` | 401 Unauthorized | `401 Unauthorized` (`code: "UNAUTHORIZED"`, "Missing authentication token") | Pass |
| **Access with Bad Token** | `GET /products` | 401 Unauthorized | `401 Unauthorized` (`code: "UNAUTHORIZED"`, "Invalid authentication token") | Pass |
| **Duplicate Email Signup** | `POST /auth/signup` | 409 Conflict | `409 Conflict` (`code: "EMAIL_TAKEN"`, "This email is already registered") | Pass |
| **Login Wrong Password** | `POST /auth/login` | 401 Unauthorized | `401 Unauthorized` (`code: "INVALID_CREDENTIALS"`, "Incorrect email or password") | Pass |
| **Register Second Owner** | `POST /auth/signup` | 201 Created | `201 Created` (Returned ID 3, `email: owner2@example.test`) | Pass |
| **Login Second Owner** | `POST /auth/login` | 200 OK | `200 OK` (Returned JWT for User ID 3) | Pass |

---

## 3. Security Payload Verification Examples

### Signup Response (No Password Hash Exposed)
```json
HTTP/1.1 201 Created
{
  "id": 2,
  "email": "owner1@example.test",
  "role": "owner",
  "created_at": "2026-10-20T19:01:04.809132Z"
}

HTTP/1.1 201 Created
{
  "name": "Paracetamol 500mg",
  "generic_name": "Acetaminophen",
  "category": "Pain Relief",
  "unit": "tablet",
  "reorder_level": 50,
  "id": 1,
  "owner_id": 2,
  "created_at": "2026-10-20T19:05:44.113397Z"
}

HTTP/1.1 401 Unauthorized
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing authentication token"
  }
}

## 4. Relationships & Adjustments Verification (Task 2.2)

| Check | Target Route | Expected Result | Actual Result / Response | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Create Supplier** | `POST /suppliers` | 201 Created | `201 Created` (ID 1, email validated) | Pass |
| **Create Batch** | `POST /batches` | 201 Created | `201 Created` (`quantity_remaining` defaulted to 100) | Pass |
| **Expiring Soon Query** | `GET /batches/expiring-soon`| 200 OK | `200 OK` (Returned newly created batch) | Pass |
| **Valid Stock Adjustment** | `POST /batches/1/adjustments` | 201 Created | `201 Created` (Deducted 5 units) | Pass |
| **Invalid Stock Adjustment**| `POST /batches/1/adjustments` | 409 Conflict | `409 Conflict` (`INSUFFICIENT_STOCK`) | Pass |
| **Adjustment History** | `GET /batches/1/adjustments` | 200 OK | `200 OK` (Returned list containing the -5 adjustment) | Pass |