from datetime import datetime, timedelta
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

    date_in_3_days = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d")
    assert response.json()["entries"][0]["date_of_next_send"] == date_in_3_days


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
    assert response.json()["category"] == "Test Category"


def test_is_paused(client, normal_user_token_headers):
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "date_of_next_send": yesterday,
    }
    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get(f"/links/1", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["date_of_next_send"] == yesterday


def test_get_link_shows_days_as_today(client, normal_user_token_headers):
    todays_date = datetime.today().strftime("%Y-%m-%d")
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "date_of_next_send": todays_date,
    }
    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get(f"/links/1", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["date_of_next_send"] == todays_date


def test_get_link_shows_days_as_tomorrow(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "date_of_next_send": (datetime.today() + timedelta(days=1)).strftime(
            "%Y-%m-%d"
        ),
    }
    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get(f"/links/1", headers=normal_user_token_headers)
    assert response.status_code == 200

    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    assert response.json()["date_of_next_send"] == tomorrow


def test_get_link_returns_not_found(client, normal_user_token_headers):
    response = client.get("/links/1", headers=normal_user_token_headers)
    assert response.status_code == 404
    assert response.json()["message"] == "Entry not found"


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
    assert response.json()["message"] == "Entry paused"


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


def test_delete_link(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "category": "Test Category",
    }

    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    response = client.get("/links", headers=normal_user_token_headers)
    assert len(response.json()["entries"]) == 1

    response = client.delete("/links/1", headers=normal_user_token_headers)
    assert response.status_code == 200

    response = client.get("/links", headers=normal_user_token_headers)
    assert len(response.json()["entries"]) == 0


def test_update_links(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "category": "Test Category",
    }

    response = client.post(
        "/links/", json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 201

    new_data = {
        "entry_title": "TestUpdate",
        "content": "http://www.testUpdate.com",
        "category": "Test Category Update",
    }

    response = client.put(
        "/links/1", json.dumps(new_data), headers=normal_user_token_headers
    )
    assert response.status_code == 200

    response = client.get("/links", headers=normal_user_token_headers)
    assert response.json()["entries"][0]["entry_title"] == "TestUpdate"


def test_update_links_returns_not_found(client, normal_user_token_headers):
    new_data = {
        "entry_title": "TestUpdate",
        "content": "http://www.testUpdate.com",
        "category": "Test Category Update",
    }

    response = client.put(
        "/links/1", json.dumps(new_data), headers=normal_user_token_headers
    )
    assert response.status_code == 404
