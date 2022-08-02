from pydantic import BaseModel

class MessageResponse(BaseModel):
  message: str
  
  class Config:
    schema_extra = {
      "example": {
        "message": "Hello, world!"
      }
    }