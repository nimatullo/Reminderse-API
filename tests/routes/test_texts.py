import json
from datetime import datetime, timedelta

from core.api.response import response


def test_text_create_with_category(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "category": "Test Category",
        "date_of_next_send": "2020-05-25",
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Text entry created"

    response = client.get("/texts", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entries"][0]["entry_title"] == "Test"
    assert response.json()["entries"][0]["category"] == "Test Category"


def test_text_create_without_category(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "date_of_next_send": "2020-05-25",
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Text entry created"

    response = client.get("/texts", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entries"][0]["entry_title"] == "Test"
    assert response.json()["entries"][0]["category"] == None


def test_text_create_without_date(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "category": "Test Category",
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Text entry created"

    response = client.get("/texts", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entries"][0]["days"] == 3


def test_get_text(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "category": "Test Category",
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get("/texts/1", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entry_title"] == "Test"
    assert response.json()["content"] == "Test"
    assert response.json()["category"] == "Test Category"


def test_get_text_not_found(client, normal_user_token_headers):
    response = client.get("/texts/1", headers=normal_user_token_headers)
    assert response.status_code == 404
    assert response.json()["message"] == "Entry not found"


def test_get_text_shows_days_as_today(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "date_of_next_send": datetime.today().strftime("%Y-%m-%d"),
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get(f"/texts/1", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["days"] == "Today"


def test_get_text_shows_days_as_tomorrow(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "date_of_next_send": (datetime.today() + timedelta(days=1)).strftime(
            "%Y-%m-%d"
        ),
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get(f"/texts/1", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["days"] == "Tomorrow"


def test_is_paused(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Tests",
        "date_of_next_send": "2020-05-25",
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get(f"/texts/1", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["days"] == "Paused"


def test_pause_text(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "category": "Test Category",
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.put("/texts/1/pause", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Entry paused"


def test_pause_text_not_found(client, normal_user_token_headers):
    response = client.put("/texts/1/pause", headers=normal_user_token_headers)
    assert response.status_code == 404
    assert response.json()["message"] == "Entry not found"


def test_resume_text(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "category": "Test Category",
        "date_of_next_send": "2020-05-25",
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.put("/texts/1/resume", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Entry resumed"


def test_resume_text_not_found(client, normal_user_token_headers):
    response = client.put("/texts/1/resume", headers=normal_user_token_headers)
    assert response.status_code == 404
    assert response.json()["message"] == "Entry not found"


def test_delete_text(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "category": "Test Category",
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get("/texts", headers=normal_user_token_headers)
    assert len(response.json()["entries"]) == 1

    response = client.delete("/texts/1", headers=normal_user_token_headers)
    assert response.status_code == 200

    response = client.get("/texts", headers=normal_user_token_headers)
    assert len(response.json()["entries"]) == 0


def test_update_text(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "Test",
        "category": "Test Category",
    }
    response = client.post(
        "/texts/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    new_data = {
        "entry_title": "Test2",
        "content": "Test2",
        "category": "Test Category2",
    }

    response = client.put(
        "/texts/1", json.dumps(new_data), headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Entry updated"

    response = client.get("/texts/1", headers=normal_user_token_headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["entry_title"] == new_data["entry_title"]


def test_update_text_not_found(client, normal_user_token_headers):
    new_data = {
        "entry_title": "Test2",
        "content": "Test2",
        "category": "Test Category2",
    }

    response = client.put(
        "/texts/1", json.dumps(new_data), headers=normal_user_token_headers
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Entry not found"
