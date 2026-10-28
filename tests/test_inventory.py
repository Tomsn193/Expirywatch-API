import pytest

@pytest.fixture
def auth_headers(client):
    client.post("/auth/signup", json={"email": "inventory@example.com", "password": "strongpassword123"})
    resp = client.post("/auth/login", json={"email": "inventory@example.com", "password": "strongpassword123"})
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}

def test_adjustment_insufficient_stock(client, auth_headers):
    # 1. Setup: Create Product, Supplier, and a Batch with 10 items
    p_res = client.post("/products", headers=auth_headers, json={"name": "Test Med", "category": "tab", "unit": "box", "reorder_level": 5})
    s_res = client.post("/suppliers", headers=auth_headers, json={"name": "Test Supplier", "email": "test@example.com"})
    
    b_res = client.post("/batches", headers=auth_headers, json={
        "product_id": p_res.json()["id"], 
        "supplier_id": s_res.json()["id"], 
        "batch_number": "BATCH-TEST-01", 
        "quantity_received": 10, 
        "expiry_date": "2027-01-01", 
        "received_date": "2026-01-01"
    })
    batch_id = b_res.json()["id"]

    # 2. Action: Try to sell 50 items (more than the 10 in stock)
    adj_res = client.post(f"/batches/{batch_id}/adjustments", headers=auth_headers, json={
        "quantity_change": -50, 
        "reason": "sold"
    })
    
    # 3. Assert: The API should block this and return 409 INSUFFICIENT_STOCK
    assert adj_res.status_code == 409
    assert adj_res.json()["error"]["code"] == "INSUFFICIENT_STOCK"