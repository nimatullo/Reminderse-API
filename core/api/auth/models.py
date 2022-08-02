from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "hello@reminderse.com",
                "password": "123456"
            }
        }

class LoginResponse(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)
    id: str = Field(...)
    interval: int = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "username": "reminderse_user",
                "email": "hello@reminerse.com",
                "id": "915ecf17-7167-465b-9456-989dea6e1e8d",
                "interval": 3
            }
        }


class RegisterRequest(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "hello@reminderse.com",
                "username": "reminderse_user",
                "password": "123456"
            }
        }


class AccessTokenSchema(BaseModel):
    access_token: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiaGVsbG9AZ21haWwuY29tIiwiZXhwIjoxNjUxNzc2MDEyLjkyMzYxMjh9.lHJcOhZDxwqQWr5-3_Sd5t3WgRkbIcV7QAE6mWyVqvo"
            }
        }
