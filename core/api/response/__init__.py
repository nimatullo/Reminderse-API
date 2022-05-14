from fastapi.responses import JSONResponse
from json import dumps
from fastapi.encoders import jsonable_encoder


def response(payload, status_code):
    return JSONResponse(content=jsonable_encoder(payload), status_code=status_code)
