from pydantic import BaseModel


class UsernameChangeRequest(BaseModel):
    username: str
    
    class Config:
        schema_extras = {
            "example": {
                "username": "new_reminderse_username"
            }
        }