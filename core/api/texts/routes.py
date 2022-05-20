import traceback

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from core.api.entries.models import EntryResponse, NewEntryRequest, UpdateEntryRequest
from core.api.entries.service import EntryService
from core.api.texts.service import TextService
from core.database.models import Text
from core.api.schemas.generic_response import MessageResponse
from core.database.database import get_db
from core.api.exceptions.RouteErrorHandler import RouteErrorHandler


texts = APIRouter(route_class=RouteErrorHandler)


@texts.post("/")
def add(
    newEntryRequest: NewEntryRequest,
    db: get_db = Depends(),
    Authenticate: AuthJWT = Depends(),
):
    Authenticate.jwt_required()
    try:
        USER = Authenticate.get_raw_jwt()
        return TextService(db).add_text(newEntryRequest, USER)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@texts.get("/")
def get_all(db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).get_all(model=Text, user_id=USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@texts.get("/{text_id}", response_model=EntryResponse)
def get(text_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).get(model=Text, id=text_id, user_id=USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@texts.delete("/{text_id}")
def delete(text_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).delete(model=Text, id=text_id, user_id=USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@texts.put("/{text_id}", response_model=MessageResponse)
def update(
    text_id: int,
    updateEntryRequest: UpdateEntryRequest,
    db: get_db = Depends(),
    Authenticate: AuthJWT = Depends(),
):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).update(
            model=Text,
            id=text_id,
            user_id=USER_ID,
            updateEntryRequest=updateEntryRequest,
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@texts.put("/{text_id}/pause")
def pause(text_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).pause(model=Text, id=text_id, user_id=USER_ID)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@texts.put("/{text_id}/resume")
def resume(text_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).resume(model=Text, id=text_id, user_id=USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
