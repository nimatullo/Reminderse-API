from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi_jwt_auth import AuthJWT

from core.database.database import get_db
from core.api.users.service import UserService
from core.api.exceptions.RouteErrorHandler import RouteErrorHandler

from core.api.users.models import UsernameChangeRequest, EmailChangeRequest, PasswordChangeRequest, IntervalChangeRequest
from core.api.schemas.generic_response import MessageResponse

me = APIRouter(route_class=RouteErrorHandler)

@me.put("/username", response_model=MessageResponse)
async def change_username(usernameChangeRequest: UsernameChangeRequest, db: get_db = Depends(), Authenticate: AuthJWT = Depends()) -> MessageResponse:
  Authenticate.jwt_required()
  try:
    USER_ID = Authenticate.get_jwt_subject()
    return UserService(db).update_username(usernameChangeRequest.username, USER_ID)
  except Exception as e:
    print(e)
    raise HTTPException(status_code=400, detail=str(e))

@me.put("/email", response_model=MessageResponse)
async def change_email(emailChangeRequest: EmailChangeRequest, db: get_db = Depends(), Authenticate: AuthJWT = Depends()) -> MessageResponse:
  Authenticate.jwt_required()
  try:
    USER_ID = Authenticate.get_jwt_subject()
    return UserService(db).update_email(emailChangeRequest.email, USER_ID)
  except Exception as e:
    print(e)
    raise HTTPException(status_code=400, detail=str(e))

@me.put("/password", response_model=MessageResponse)
async def change_password(passwordChangeRequest: PasswordChangeRequest, db: get_db = Depends(), Authenticate: AuthJWT = Depends()) -> MessageResponse:
  Authenticate.jwt_required()
  try:
    USER_ID = Authenticate.get_jwt_subject()
    return UserService(db).update_password(passwordChangeRequest.password, USER_ID)
  except Exception as e:
    print(e)
    raise HTTPException(status_code=400, detail=str(e))

@me.put("/interval", response_model=MessageResponse)
async def change_interval(intervalChangeRequest: IntervalChangeRequest, db: get_db = Depends(), Authenticate: AuthJWT = Depends()) -> MessageResponse:
  Authenticate.jwt_required()
  try:
    USER_ID = Authenticate.get_jwt_subject()
    return UserService(db).update_interval(intervalChangeRequest.interval, USER_ID)
  except Exception as e:
    print(e)
    raise HTTPException(status_code=400, detail=str(e))
