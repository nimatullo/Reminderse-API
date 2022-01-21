from datetime import timedelta
from os import access
from flasktest.email import send_confirmation
from flasktest.users.repo.repo import UserRepository
from flask import make_response, jsonify
from flasktest import bcrypt, ts
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    jwt_refresh_token_required, get_jwt_identity, jwt_required, unset_jwt_cookies


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    def signup(self, username, email, password):
        if self.repo.username_exists(username):
            return make_response(jsonify({"message": "Username already exists"}), 400)
        if self.repo.email_exists(email):
            return make_response(jsonify({"message": "Email already exists"}), 400)

        hashed_password = bcrypt.generate_password_hash(
            password).decode("utf8")

        result = self.repo.add(username, email, hashed_password)

        if result:
            self.send_confirmation_email(email)
            return make_response(jsonify({"message": "Successful signup!"}), 201)
        else:
            return make_response(jsonify({"message": "Server error"}), 500)

    def set_email_to_confirm(self, email):
        result = self.repo.set_email_to_confirmed(email)

        if result:
            return make_response(jsonify({"message": "Email confirmed"}), 200)
        else:
            return make_response(jsonify({"message": "Server error"}), 500)

    def login(self, email, password):
        user = self.repo.get_userinfo_email(email)

        if user and self.is_password_correct(user.password, password):
            token_expiration = timedelta(days=7)
            access_token = create_access_token(
                identity=user.id,
                expires_delta=token_expiration
            )
            refresh_token = create_refresh_token(identity=user.id)
            response = jsonify({
                "username": user.username,
                "email": user.email,
                "id": user.id,
            })
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return make_response(response, 200)
        else:
            return make_response(jsonify({
                "message": "Incorrect log in credentials"
            }),
                401)

    def refresh_token(self, current_user):
        token_expiration = timedelta(days=7)
        access_token = create_refresh_token(
            identity=current_user,
            expires_delta=token_expiration
        )
        response = jsonify({
            "refreshed": True
        })
        set_access_cookies(response, access_token)
        return make_response(response, 200)

    def update_username(self, new_username, current_user):
        if self.repo.username_exists(new_username):
            return make_response(jsonify({
                "message": "Username is already taken",
            }), 400)
        elif current_user.username is not new_username:
            if self.repo.change_username(current_user.id, new_username):
                return make_response(jsonify({
                    "message": "Changes saved"
                }), 200)
            else:
                return make_response(jsonify({
                    "message": "Server error"
                }), 500)

    def update_email(self, new_email, current_user):
        if self.repo.email_exists(new_email):
            return make_response(jsonify({
                "message": "Email is already taken"
            }), 400)
        elif current_user.email is not new_email:
            if self.repo.change_email(current_user.id, new_email):
                self.send_confirmation_email(new_email)
                return make_response(jsonify({
                    "message": "Changes saved"
                }), 200)
            else:
                return make_response(jsonify({
                    "message": "Server error"
                }), 500)

    def update_password(self, new_password, current_user):
        new_hashed_password = bcrypt.generate_password_hash(
            new_password).decode('utf8')
        if self.repo.change_password(current_user.id, new_hashed_password):
            return make_response(jsonify({
                "message": "Changes saved"
            }))
        else:
            return make_response(jsonify({
                "message": "Server error"
            }), 500)

    def send_confirmation_email(self, email):
        token = ts.dumps(email, salt='email-confirm-key')
        html_mid = f'''
                <p> <a href="https://www.reminderse.com/confirm-email/{token}">Confirm Email</a></p>
                '''
        try:
            send_confirmation(email, html_mid)
            return make_response({"message": "Email sent successfully"}, 200)
        except Exception as e:
            return make_response(jsonify({
                "message": "Server error",
                "error": str(e)
            }), 500)

    def is_password_correct(self, saved_password_hash, entered_password):
        return bcrypt.check_password_hash(saved_password_hash, entered_password)

    def get_current_user(self):
        current_user_id = get_jwt_identity()
        return self.repo.get_userinfo_id(current_user_id)
