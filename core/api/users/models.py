from pydantic import BaseModel, EmailStr


class UsernameChangeRequest(BaseModel):
    username: str
    
    class Config:
        schema_extras = {
            "example": {
                "username": "new_reminderse_username"
            }
        }

class EmailChangeRequest(BaseModel):
    email: EmailStr
    
    class Config:
        schema_extras = {
            "example": {
                "email": "new-email@reminderse.com"
            }
        }
        
class PasswordChangeRequest(BaseModel):
    password: str
    
    class Config:
        schema_extras = {
            "example": {
                "password": "new_password"
            }
        }
        
class IntervalChangeRequest(BaseModel):
    interval: int
    
    class Config:
        schema_extras = {
            "example": {
                "interval": 5
            }
        }