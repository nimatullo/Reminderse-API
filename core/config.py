from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "Reminderse API"
    authjwt_secret_key: str = "super-secret-key"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
    SECRET_KEY: str = "secret"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # minutes


settings = Settings()
