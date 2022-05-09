from tkinter import CURRENT
from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from core.database.database import get_db
from core.api.users.service import UserService

from core.api.users.models import UsernameChangeRequest

me = APIRouter()

@me.put("/username")
async def change_username(usernameChangeRequest: UsernameChangeRequest, db: get_db = Depends(), 
                          Authenticate: AuthJWT = Depends()):
  Authenticate.jwt_required()
  try:
    USER_ID = Authenticate.get_jwt_subject()
    return UserService(db).update_username(usernameChangeRequest.username, USER_ID)
  except Exception as e:
    print(e)
    raise HTTPException(status_code=400, detail=str(e))