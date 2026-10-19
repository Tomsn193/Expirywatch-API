# ExpiryWatch API: Data Model

**Database:** PostgreSQL  
**Status:** Week 2 implements `users`, `suppliers`, `batches` and `stock_adjustments`, and adds ownership to Week 1 `products`.  
**Data policy:** dummy data only. No real personal, supplier or patient information.

---

## 1. Entities at a glance

| Entity | Purpose |
|---|---|
| `users` | The pharmacy owners who log in and own records |
| `products` | The medicines/items the pharmacy sells (the catalogue) |
| `suppliers` | Who the pharmacy buys stock from |
| `batches` | A delivery of one product from one supplier, with its own expiry date |
| `stock_adjustments` | An audit trail of every change to a batch's quantity |

---

## 2. Entity definitions

### 2.1 `users` (added in Week 2)

| Field | Type | Required? | Constraints / purpose |
|---|---|---|---|
| `id` | Integer | Yes | Primary key. |
| `email` | String(255) | Yes | Unique. Store lowercase. Dummy addresses only. |
| `password_hash` | String(255) | Yes | Stores bcrypt hash. Plain passwords are never stored. |
| `role` | String(20) | Yes | Default `owner`. |
| `created_at` | Timestamp with time zone | Yes | Set automatically. |

### 2.2 `products` (updated in Week 2)

| Field | Type | Required? | Constraints / purpose |
|---|---|---|---|
| `id` | Integer | Yes | Primary key. |
| `owner_id` | Integer (FK) | Yes | References `users.id`. Defines who owns the record. |
| `name` | String(150) | Yes | Display name. Cannot be blank. |
| `generic_name` | String(150) | No | Optional generic/ingredient label. |
| `category` | String(80) | Yes | Simple category label. |
| `unit` | String(30) | Yes | How stock is counted: `tablet`, `bottle`, `sachet`, `pack`. |
| `reorder_level` | Integer | Yes | Default `0`. Must be `>= 0`. |
| `created_at` | Timestamp with time zone | Yes | Set automatically. |

### 2.3 `suppliers` (planned for Week 2)

| Field | Type | Required? | Constraints / purpose |
|---|---|---|---|
| `id` | Integer | Yes | Primary key. |
| `owner_id` | Integer (FK) | Yes | References `users.id`. Defines who owns the record. |
| `name` | String(150) | Yes | Dummy supplier/business name. |
| `phone` | String(30) | No | Stored as text (preserves leading zeros and `+`). |
| `email` | String(254) | No | Dummy addresses. |
| `created_at` | Timestamp with time zone | Yes | Set automatically. |

### 2.4 `batches` (planned for Week 2)

| Field | Type | Required? | Constraints / purpose |
|---|---|---|---|
| `id` | Integer | Yes | Primary key. |
| `product_id` | Integer (FK) | Yes | References `products.id`. |
| `supplier_id` | Integer (FK) | Yes | References `suppliers.id`. |
| `batch_number` | String(60) | Yes | Batch identifier. Unique per supplier. |
| `quantity_received` | Integer | Yes | Must be `> 0`. |
| `quantity_remaining` | Integer | Yes | Starts equal to `quantity_received`; must never be negative. |
| `expiry_date` | Date | Yes | Belongs to the batch. Must be later than `received_date`. |
| `received_date` | Date | Yes | Date the batch was received. |

### 2.5 `stock_adjustments` (planned for Week 2)

| Field | Type | Required? | Constraints / purpose |
|---|---|---|---|
| `id` | Integer | Yes | Primary key. |
| `batch_id` | Integer (FK) | Yes | References `batches.id`. |
| `quantity_change` | Integer | Yes | Non-zero. Negative removes stock, positive adds/corrects. |
| `reason` | String(30) | Yes | One of `sold`, `damaged`, `expired`, `correction`. |
| `note` | String(255) | No | Optional explanation. |
| `created_at` | Timestamp with time zone | Yes | Set automatically. |

---

## 3. Relationships

| Relationship | Cardinality | Notes |
|---|---|---|
| user -> products | One-to-many | A user owns many products. |
| user -> suppliers | One-to-many | A user owns many suppliers. |
| product -> batches | One-to-many | A product can arrive in many batches. |
| supplier -> batches | One-to-many | A supplier can supply many batches. |
| batch -> stock_adjustments | One-to-many | A batch can have many adjustments. |

### ERD (Mermaid)

```mermaid
erDiagram
    USERS ||--o{ PRODUCTS : "owns"
    USERS ||--o{ SUPPLIERS : "owns"
    PRODUCTS ||--o{ BATCHES : "arrives as"
    SUPPLIERS ||--o{ BATCHES : "supplies"
    BATCHES ||--o{ STOCK_ADJUSTMENTS : "has"

    USERS {
        int id PK
        string email
        string password_hash
        string role
        timestamptz created_at
    }
    PRODUCTS {
        int id PK
        int owner_id FK
        string name
        string generic_name
        string category
        string unit
        int reorder_level
        timestamptz created_at
    }
    SUPPLIERS {
        int id PK
        int owner_id FK
        string name
        string phone
        string email
        timestamptz created_at
    }
    BATCHES {
        int id PK
        int product_id FK
        int supplier_id FK
        string batch_number
        int quantity_received
        int quantity_remaining
        date expiry_date
        date received_date
    }
    STOCK_ADJUSTMENTS {
        int id PK
        int batch_id FK
        int quantity_change
        string reason
        string note
        timestamptz created_at
    }