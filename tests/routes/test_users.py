import json
from core.email.send_email import fm
fm.config.SUPPRESS_SEND = 1

# def test_email_confirmed(client):
#   data = {
#     "email": "testing@reminderse.com",
#     "username": "test",
#     "password": "test"   
#   }
#   response = client.post("/signup", json.dumps(data))
#   assert response.status_code == 200
#   response 

def test_change_username(client, normal_user_token_headers):
  data = {
    "username": "bingus",
  }
  response = client.put("/username", json.dumps(data), headers=normal_user_token_headers)
  assert response.status_code == 200
  assert response.json()["message"] == "Changes saved"

def test_change_username_with_existing_username(client, normal_user_token_headers):
  data = {
    "username": "test"
  }
  response = client.put("/username", json.dumps(data), headers=normal_user_token_headers)
  assert response.status_code == 400
  assert response.json()["detail"] == "Username already exists"

def test_change_email(client, normal_user_token_headers):
  data = {
    "email": "test1@reminderse.com",
  }
  response = client.put("/email", json.dumps(data), headers=normal_user_token_headers)
  assert response.status_code == 200
  assert response.json()["message"] == "Changes saved"

def test_change_email_with_existing_email(client, normal_user_token_headers):
  data = {
    "email": "testing@reminderse.com"
  }
  response = client.put("/email", json.dumps(data), headers=normal_user_token_headers)
  assert response.status_code == 400
  assert response.json()["detail"] == "Email already exists"

def test_change_password(client, normal_user_token_headers):
  data = {
    "password": "test1"
  }
  response = client.put("/password", json.dumps(data), headers=normal_user_token_headers)
  assert response.status_code == 200
  assert response.json()["message"] == "Changes saved"
  data = {
    "email": "testing@reminderse.com",
    "password": data.get("password")
  }
  response = client.post("/login", json.dumps(data))
  assert response.status_code == 200

def test_change_interval(client, normal_user_token_headers):
  data = {
    "interval": "5"
  }
  response = client.put("/interval", json.dumps(data), headers=normal_user_token_headers)
  assert response.status_code == 200
  assert response.json()["message"] == "Changes saved"

def test_token_required(client):
  protected_endpoints = [
    "/username",
    "/email",
    "/password",
    "/interval"
  ]
  data = {}
  
  for endpoint in protected_endpoints:
    if endpoint == "/username":
      data = {
        "username": "bingus"
      }
    elif endpoint == "/email":
      data = {
        "email": "test1@reminderse.com"
      }
    elif endpoint == "/password":
      data = {
        "password": "test1"
      }
    elif endpoint == "/interval":
      data = {
        "interval": 5
      }
    
    response = client.put(endpoint, json.dumps(data))
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing Authorization Header"
        
  