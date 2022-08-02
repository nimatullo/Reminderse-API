import json, pytest
from core.email.send_email import fm

fm.config.SUPPRESS_SEND = 1


def test_register_user(client):
    data = {"email": "test@reminderse.com", "username": "test", "password": "test"}
    response = client.post("/signup", json.dumps(data))
    assert response.status_code == 201
    assert response.json()["message"] == "User created"


def test_register_user_with_existing_username(client):
    data = {"email": "test@reminderse.com", "username": "test", "password": "test"}
    response = client.post("/signup", json.dumps(data))
    response = client.post("/signup", json.dumps(data))
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_register_user_with_existing_email(client):
    data = {"email": "test@reminderse.com", "username": "test", "password": "test"}
    response = client.post("/signup", json.dumps(data))
    data["username"] = "test2"
    response = client.post("/signup", json.dumps(data))
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


def test_register_sends_confirmation_email(client):
    data = {"email": "test@reminderse.com", "username": "test", "password": "test"}
    fm.config.SUPPRESS_SEND = 1
    with fm.record_messages() as outbox:
        response = client.post("/signup", json.dumps(data))
        assert response.status_code == 201
        assert response.json()["message"] == "User created"
        assert len(outbox) == 1
        assert outbox[0]["To"] == data["email"]


def test_login_user(client):
    register_data = {
        "email": "test@reminderse.com",
        "username": "test",
        "password": "test",
    }
    response = client.post("/signup", json.dumps(register_data))
    assert response.status_code == 201
    login_data = {"email": "test@reminderse.com", "password": "test"}
    response = client.post("/login", json.dumps(login_data))
    assert response.status_code == 200
    assert response.json()["email"] == login_data["email"]


def test_login_user_with_wrong_password(client):
    register_data = {
        "email": "test@reminderse.com",
        "username": "test",
        "password": "test",
    }
    response = client.post("/signup", json.dumps(register_data))
    assert response.status_code == 201
    login_data = {"email": "test@reminderse.com", "password": "wrongpassword"}
    response = client.post("/login", json.dumps(login_data))
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"
