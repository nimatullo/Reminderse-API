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
    assert response.status_code == 200
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
    assert response.status_code == 200
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
    print(response.json())
    assert response.status_code == 200
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
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Link entry created"

    response = client.get("/links", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["entries"][0]["url"] == "https://www.test.com"
