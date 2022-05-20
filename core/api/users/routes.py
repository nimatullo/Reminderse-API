from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi_jwt_auth import AuthJWT
from itsdangerous import URLSafeTimedSerializer

from core.email.send_email import send
from core.database.database import get_db
from core.api.users.service import UserService
from core.api.exceptions.RouteErrorHandler import RouteErrorHandler

from core.api.users.models import (
    UsernameChangeRequest,
    EmailChangeRequest,
    PasswordChangeRequest,
    IntervalChangeRequest,
)
from core.api.schemas.generic_response import MessageResponse

ts = URLSafeTimedSerializer("super-secret-key")

me = APIRouter(route_class=RouteErrorHandler)


@me.put("/username", response_model=MessageResponse)
async def change_username(
    usernameChangeRequest: UsernameChangeRequest,
    db: get_db = Depends(),
    Authenticate: AuthJWT = Depends(),
) -> MessageResponse:
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return UserService(db).update_username(usernameChangeRequest.username, USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@me.put("/email", response_model=MessageResponse)
async def change_email(
    emailChangeRequest: EmailChangeRequest,
    db: get_db = Depends(),
    Authenticate: AuthJWT = Depends(),
) -> MessageResponse:
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return UserService(db).update_email(emailChangeRequest.email, USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@me.get("/confirmed", response_model=MessageResponse)
async def is_email_confirmed(
    db: get_db = Depends(), Authenticate: AuthJWT = Depends()
) -> MessageResponse:
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return UserService(db).is_email_confirmed(USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@me.put("/password", response_model=MessageResponse)
async def change_password(
    passwordChangeRequest: PasswordChangeRequest,
    db: get_db = Depends(),
    Authenticate: AuthJWT = Depends(),
) -> MessageResponse:
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return UserService(db).update_password(passwordChangeRequest.password, USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@me.put("/interval", response_model=MessageResponse)
async def change_interval(
    intervalChangeRequest: IntervalChangeRequest,
    db: get_db = Depends(),
    Authenticate: AuthJWT = Depends(),
) -> MessageResponse:
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return UserService(db).update_interval(intervalChangeRequest.interval, USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@me.get("/send-confirmation-email", response_model=MessageResponse)
async def send_confirmation_email(
    background_tasks: BackgroundTasks,
    db: get_db = Depends(),
    Authenticate: AuthJWT = Depends(),
) -> MessageResponse:
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        user_email = UserService(db).get_user_email(USER_ID)
        background_tasks.add_task(
            send,
            user_email,
            {"token": ts.dumps(user_email, salt="email-confirmation-salt")},
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@me.get("/confirm-email/{token}", response_model=MessageResponse)
async def confirm_email(token, db: get_db = Depends()) -> MessageResponse:
    email = ts.loads(token, salt="email-confirmation-salt", max_age=1440)
    return UserService(db).user_email_confirmed(email)
