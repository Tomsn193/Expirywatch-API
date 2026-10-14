# Week 1 Test Results

| Check | Expected result | Actual result |
| :--- | :--- | :--- |
| Create a valid product | 201; returned product includes generated id and created_at | Pass: Returned 201 Created with ID 4 |
| List products | 200; list includes seeded and created records | Pass: Returned 200 OK with 4 products |
| Get an existing ID | 200; correct product is returned | Pass: Returned 200 OK for ID 1 |
| Get a missing ID | 404; safe error response | Pass: Returned 404 Not Found for ID 9999 |
| Update an existing ID | 200; updated fields are returned | Pass: Returned 200 OK with updated name |
| Create without required fields | 400; validation error | Pass: Returned 400 Bad Request |
| Use a negative reorder_level | 400; validation error | Pass: Returned 400 Bad Request |