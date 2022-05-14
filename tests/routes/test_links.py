import json


def test_get_all(client, normal_user_token_headers):
    response = client.get("/links", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert type(response.json()["entries"]) is list


def test_add_link_with_category(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "category": "Test Category",
        "date_of_next_send": "2020-05-25",
    }
    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Link entry created"

    response = client.get("/links", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entries"][0]["entry_title"] == "Test"
    assert response.json()["entries"][0]["category"] == "Test Category"


def test_add_link_without_category(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "date_of_next_send": "2020-05-25",
    }
    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Link entry created"

    response = client.get("/links", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entries"][0]["entry_title"] == "Test"
    assert response.json()["entries"][0]["category"] == None


def test_add_link_without_date(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "category": "Test Category",
    }

    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Link entry created"

    response = client.get("/links", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entries"][0]["days"] == 3


def test_add_link_with_http_upgraded(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "www.test.com",
    }

    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Link entry created"

    response = client.get("/links", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entries"][0]["url"] == "https://www.test.com"


def test_get_link(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "category": "Test Category",
    }

    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get(f"/links/1", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entry_title"] == "Test"
    assert response.json()["category"]["title"] == "Test Category"


def test_get_link_returns_not_found(client, normal_user_token_headers):
    response = client.get("/links/1", headers=normal_user_token_headers)
    assert response.status_code == 404
    assert response.json()["message"] == "Link not found"


def test_pause_link(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "category": "Test Category",
    }
    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.put(f"/links/1/pause", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Link paused"


def test_pause_link_returns_not_found(client, normal_user_token_headers):
    response = client.put("/links/1/pause", headers=normal_user_token_headers)
    assert response.status_code == 404


def test_resume_link(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "category": "Test Category",
        "date_of_next_send": "2020-05-25",
    }
    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.put(f"/links/1/resume", headers=normal_user_token_headers)
    assert response.status_code == 200


def test_resume_link_returns_not_found(client, normal_user_token_headers):
    response = client.put("/links/1/resume", headers=normal_user_token_headers)
    assert response.status_code == 404
