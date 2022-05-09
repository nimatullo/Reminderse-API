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

