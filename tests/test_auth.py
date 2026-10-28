def test_signup_success(client):
    response = client.post(
        "/auth/signup",
        json={"email": "testuser@example.com", "password": "strongpassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    assert "password" not in data  # Ensure we never leak the password

def test_signup_duplicate_email(client):
    # Register the first time
    client.post(
        "/auth/signup",
        json={"email": "duplicate@example.com", "password": "strongpassword123"}
    )
    # Attempt to register with the exact same email
    response = client.post(
        "/auth/signup",
        json={"email": "duplicate@example.com", "password": "differentpassword"}
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "EMAIL_TAKEN"

def test_login_success(client):
    # Setup: Create a user first
    client.post(
        "/auth/signup",
        json={"email": "loginuser@example.com", "password": "strongpassword123"}
    )
    # Action: Log in
    response = client.post(
        "/auth/login",
        json={"email": "loginuser@example.com", "password": "strongpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    # Setup: Create a user first
    client.post(
        "/auth/signup",
        json={"email": "wrongpass@example.com", "password": "strongpassword123"}
    )
    # Action: Log in with the wrong password
    response = client.post(
        "/auth/login",
        json={"email": "wrongpass@example.com", "password": "incorrectpassword"}
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"