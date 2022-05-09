from core.api.users.repo import UserRepository
import bcrypt

from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

class UserService:
    def __init__(self, db) -> None:
        self.repo = UserRepository(db)

    def signup(self, username, email, password):
        if self.repo.username_exists(username):
            raise Exception("Username already exists")
        if self.repo.email_exists(email):
            raise Exception("Email already exists")

        hashed_password = bcrypt.hashpw(password.encode(
            'utf8'), bcrypt.gensalt())

        result = self.repo.add(username, email, hashed_password.decode('utf8'))

        if result:
            return {"message": "User created"}
        else:
            raise Exception("Server error")

    def set_email_to_confirm(self, email):
        result = self.repo.set_email_to_confirmed(email)

        if result:
            return {"message": "Email confirmed"}
        else:
            raise Exception("Server error")

    def login(self, email, password, Authorize: AuthJWT):
        user = self.authenticate(email, password)
        if not user:
            raise Exception("Invalid credentials")
        
        access_token = Authorize.create_access_token(
            subject=str(user.id)
        )
        
        response = JSONResponse(content={
            "username": user.username,
            "email": user.email,
            "id": str(user.id),
            "interval": user.interval,
            "token": access_token
        })
        response.set_cookie(key="token", value=access_token)
        return response
    
    def authenticate(self, email: str, password: str):
        user = self.repo.get_userinfo_email(email)
        print(f'The found user: {user}')
        if not user:
            return False
        if not self.is_password_correct(user.password, password):
            return False
        return user
    
    def update_username(self, new_username, current_user_id):
        if self.repo.username_exists(new_username):
            raise Exception("Username already exists")
        
        user = self.repo.get_userinfo_id(current_user_id)
        
        if user.username is not new_username:
            if self.repo.change_username(current_user_id, new_username):
                return {
                    "message": "Changes saved"
                }
            else:
                raise Exception("Server error")

    def update_email(self, new_email, current_user_id):
        if self.repo.email_exists(new_email):
            raise Exception("Email already exists")
        
        user = self.repo.get_userinfo_id(current_user_id)
        
        if user.email is not new_email:
            if self.repo.change_email(current_user_id, new_email):
                return {
                    "message": "Changes saved"
                }
            else:
                raise Exception("Server error")

    def update_password(self, new_password, current_user_id):
        new_hashed_password = bcrypt.hashpw(
            new_password.encode('utf8'), bcrypt.gensalt())
        
        if self.repo.change_password(current_user_id, new_hashed_password.decode('utf8')):
            return {
                "message": "Changes saved"
            }
        else:
            return {
                "message": "Server error"
            }

    def update_interval(self, new_interval, current_user_id):
        if self.repo.change_interval(new_interval, current_user_id):
            return {
                "message": "Changes saved"
            }
        else:
            return {
                "message": "Server error"
            }

    def is_password_correct(self, saved_password_hash, entered_password):
        return bcrypt.checkpw(entered_password.encode('utf8'), saved_password_hash.encode('utf8'))