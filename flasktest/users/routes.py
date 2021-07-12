import datetime
from flasktest.users.service.service import UserService

from flask import Blueprint
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    jwt_refresh_token_required, get_jwt_identity, jwt_required, unset_jwt_cookies
from flask_login import logout_user

from flasktest import db, bcrypt, ts
from flasktest.email import send_confirmation
from flasktest.models import Users, Links, Text
from flasktest.users.utils import current_user
from flasktest.users import service

users = Blueprint('users', __name__)
service = UserService()


@users.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "hello!"}), 200


@users.route('/api/register', methods=['POST'])
def post():
    CURRENT_USER = current_user(get_jwt_identity())
    if CURRENT_USER:
        return jsonify({"message": "Already Logged In."}), 400

    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    return service.signup(username=username, email=email, password=password)


@users.route('/confirm_email_token/<token>')
def confirm_email_token(token):
    email = ts.loads(token, salt='email-confirm-key', max_age=1440)
    return service.set_email_to_confirm(email)


@users.route('/api/send-email-confirmation', methods=["GET"])
@jwt_required
def request_confirmation_email():
    CURRENT_USER = current_user(get_jwt_identity())
    if CURRENT_USER.email_confirmed:
        return make_response({"message": "Email already confirmed"}, 400)
    else:
        return service.send_confirmation_email(CURRENT_USER.email)


@users.route("/token/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    CURRENT_USER = current_user(get_jwt_identity())
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(
        identity=CURRENT_USER, expires_delta=expires)
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


@users.route('/api/login', methods=["POST"])
def login():
    CURRENT_USER = current_user(get_jwt_identity())
    if CURRENT_USER:
        return make_response(jsonify({
            'message': f'Already signed in',
            'username': CURRENT_USER.username,
            'id': CURRENT_USER.id
        }), 200)

    email = request.json.get('email')
    password = request.json.get('password')
    return service.login(email, password)


@users.route('/api/logout', methods=["PUT"])
@jwt_required
def logoutmyhouse():
    response = jsonify({"message": "Logged out. Come again!"})
    unset_jwt_cookies(response)
    print("User logged out.")
    return response, 200


@users.route('/api/confirmed', methods=["GET"])
@jwt_required
def is_confirmed():
    CURRENT_USER = current_user(get_jwt_identity())
    return make_response(jsonify({"user": CURRENT_USER.username, "isConfirmed": CURRENT_USER.email_confirmed}))


@users.route('/api/change', methods=['POST'])
@jwt_required
def change_settings():
    '''
    WILL BE DEPRECATED
    '''
    CURRENT_USER = current_user(get_jwt_identity())
    email = request.json.get("email")
    username = request.json.get("username")

    return service.update_user_info(username, email, CURRENT_USER)


@users.route('/api/change/username', methods=['PUT'])
@jwt_required
def change_username():
    CURRENT_USER = current_user(get_jwt_identity())
    new_username = request.json.get("username")
    return service.update_username(new_username, CURRENT_USER)


@users.route("/api/change/email", methods=['PUT'])
@jwt_required
def change_email():
    CURRENT_USER = current_user(get_jwt_identity())
    new_email = request.json.get("email")
    return service.update_email(new_email, CURRENT_USER)


@users.route('/api/change/password', methods=['PUT'])
@jwt_required
def change_pass():
    CURRENT_USER = current_user(get_jwt_identity())
    current_password = request.json.get("current_password")
    new_password = request.json.get("new_password")

    if not service.is_password_correct(CURRENT_USER.password, current_password):
        return make_response(jsonify({
            "message": "Invalid credentials"
        }), 401)
    else:
        return service.update_password(new_password, CURRENT_USER)


@users.route("/api/unsubscribe", methods=["DELETE"])
@jwt_required
def unsub():
    CURRENT_USER = current_user(get_jwt_identity())
    links = Links.query.filter_by(user_id=CURRENT_USER.id)
    texts = Text.query.filter_by(user_id=CURRENT_USER.id)
    for link in links:
        db.session.delete(link)
    for text in texts:
        db.session.delete(text)

    db.session.delete(Users.query.filter_by(id=CURRENT_USER.id).first())
    db.session.commit()
    logout_user()

    return jsonify({
        "message": "User deleted."
    }), 200


@users.route("/api/current+user", methods=["GET"])
@jwt_required
def who_is_logged_in():
    CURRENT_USER = current_user(get_jwt_identity())
    return jsonify({
        "id": CURRENT_USER.id,
        "username": CURRENT_USER.username,
        "email": CURRENT_USER.email
    }), 200
