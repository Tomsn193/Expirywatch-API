import pytest

@pytest.fixture
def auth_headers(client):
    # Helper fixture to create a user and return their authorization headers
    client.post("/auth/signup", json={"email": "owner@example.com", "password": "strongpassword123"})
    resp = client.post("/auth/login", json={"email": "owner@example.com", "password": "strongpassword123"})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_product_success(client, auth_headers):
    response = client.post(
        "/products",
        headers=auth_headers,
        json={"name": "Test Product", "category": "tablet", "unit": "pack", "reorder_level": 10}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"

def test_create_product_unauthorized(client):
    # Attempting to create a product without the auth token
    response = client.post(
        "/products",
        json={"name": "Test Product", "category": "tablet", "unit": "pack", "reorder_level": 10}
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"

def test_get_product_not_found(client, auth_headers):
    response = client.get("/products/9999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "PRODUCT_NOT_FOUND"

def test_cross_owner_forbidden(client, auth_headers):
    # Setup: Create a product as Owner 1
    post_resp = client.post(
        "/products",
        headers=auth_headers,
        json={"name": "Owner 1 Product", "category": "tablet", "unit": "pack", "reorder_level": 10}
    )
    product_id = post_resp.json()["id"]

    # Setup: Register and log in as Owner 2
    client.post("/auth/signup", json={"email": "owner2@example.com", "password": "strongpassword123"})
    resp2 = client.post("/auth/login", json={"email": "owner2@example.com", "password": "strongpassword123"})
    token2 = resp2.json()["access_token"]
    auth_headers2 = {"Authorization": f"Bearer {token2}"}

    # Action: Owner 2 tries to fetch Owner 1's product
    get_resp = client.get(f"/products/{product_id}", headers=auth_headers2)
    
    # Assert it blocks access
    assert get_resp.status_code == 403
    assert get_resp.json()["error"]["code"] == "FORBIDDEN"