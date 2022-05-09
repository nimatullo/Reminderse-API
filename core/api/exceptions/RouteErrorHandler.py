from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute
from fastapi_jwt_auth.exceptions import MissingTokenError

class RouteErrorHandler(APIRoute):
  def get_route_handler(self) -> Callable:
    original_handler = super().get_route_handler()
    
    async def custom_handler(request: Request) -> Response:
      try:
        return await original_handler(request)
      except MissingTokenError as e:
        raise HTTPException(status_code=401, detail=str(e.message))
      except Exception as e:
        if isinstance(e, HTTPException):
          print(e)
          raise e
        raise HTTPException(status_code=500, detail=str(e))
      
    return custom_handler