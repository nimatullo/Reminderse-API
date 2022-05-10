import json


def test_get_all(client, normal_user_token_headers):
    response = client.get("/links", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert type(response.json()["entries"]) is list


def test_add_link_with_category(client, normal_user_token_headers):
    data = {
        "entry_title": "Test",
        "content": "http://www.test.com",
        "category": "Test",
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
