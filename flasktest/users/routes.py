from flask import Blueprint
from flask import url_for, request, jsonify, make_response, session
from flasktest import db, bcrypt, ts
from flasktest.models import Users, Links, Category, Text
from flasktest.email import send
from flask_login import login_user, logout_user, login_required
from flasktest import app
from flasktest.users.utils import current_user
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_refresh_token_required, get_jwt_identity, jwt_required, unset_jwt_cookies
import datetime

users = Blueprint('users', __name__)


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

    if Users.query.filter_by(username=username).first():
        return make_response(jsonify({"message": "Username exists"}), 400)
    elif Users.query.filter_by(email=email).first():
        return make_response(jsonify({"message": "Email already in use"}), 400)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
    user = Users(username=username.lower().rstrip(),
                 email=email.lower(), password=hashed_password)
    send_email_confirmation(user.email)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': f'Thank you for signing up {user.username}!'}), 201


@users.route('/confirm_email_token/<token>')
def confirm_email_token(token):
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=1440)
        user = Users.query.filter_by(email=email).first()
        user.email_confirmed = True
        db.session.commit()
        return make_response(jsonify({"message": "Email confirmed"}))
    except:
        return make_response(jsonify({"message": "failed"}), 401)


def send_email_confirmation(email):
    token = ts.dumps(email, salt='email-confirm-key')
    html_mid = f'''
                <p> <a href="https://reminderse.com/confirm-email/{token}">Confirm Email</a></p>
                '''
    send(email, html_mid)


@users.route('/api/send-email-confirmation', methods=["GET"])
@jwt_required
def request_confirmation_email():
    CURRENT_USER = current_user(get_jwt_identity())
    if CURRENT_USER.email_confirmed:
        return make_response({"message": "Email already confirmed"}, 400)
    else:
        send_email_confirmation(CURRENT_USER.email)
        return make_response({"message": "Email sent successfully"}, 200)


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

    user = Users.query.filter_by(email=email.lower().rstrip()).first()
    if user and bcrypt.check_password_hash(user.password, password):
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(
            identity=user.id, expires_delta=expires)
        refresh_token = create_refresh_token(identity=user.id)
        response = jsonify({
            'message': f'Welcome {user.username}',
            'username': user.username,
            'id': user.id,
        })
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 200
    else:
        return jsonify({'message': 'Authentification Failed'}), 401


@users.route('/api/logout', methods=["PUT"])
@jwt_required
def logoutmyhouse():
    response = jsonify({"message": "Logged out. Come again!"})
    unset_jwt_cookies(response)
    print("User logged out.")
    return response, 200


@users.route('/api/confirmed', methods=["GET"])
@jwt_required
def isConfirmed():
    CURRENT_USER = current_user(get_jwt_identity())
    return make_response(jsonify({"user": CURRENT_USER.username, "isConfirmed": CURRENT_USER.email_confirmed}))


@users.route('/api/change', methods=['POST'])
@jwt_required
def change_settings():
    CURRENT_USER = current_user(get_jwt_identity())
    email = request.json.get("email")
    username = request.json.get("username")

    # Check if username is taken
    user = Users.query.filter_by(username=username).first()

    if(user and not CURRENT_USER.username == username):
        return jsonify({"message": "Username is taken."}), 400
    else:
        CURRENT_USER.username = username

    if not CURRENT_USER.email == email:
        CURRENT_USER.email = email
        CURRENT_USER.email_confirmed = False
        send_confirmation(email)
    db.session.commit()

    return jsonify({"message": "Changes saved."}), 200


@users.route('/api/change/username', methods=['PUT'])
@jwt_required
def change_username():
    CURRENT_USER = current_user(get_jwt_identity())
    new_username = request.json.get("username")

    # Check if username is already taken
    user = Users.query.filter_by(username=new_username).first()

    if(user and not CURRENT_USER.username == new_username):
        return jsonify({"message": "Username is taken."}), 400
    else:
        CURRENT_USER.username = new_username
    db.session.commit()

    return make_response(jsonify({"message": "Username changed"}), 200)


@users.route("/api/change/email", methods=['PUT'])
@jwt_required
def change_email():
    CURRENT_USER = current_user(get_jwt_identity())
    new_email = request.json.get("email")

    if not CURRENT_USER.email == new_email:
        CURRENT_USER.email == new_email
        CURRENT_USER.email_confirmed = False

    db.session.commit()

    return make_response(jsonify({"message": "Email changed"}))


@users.route('/api/change/password', methods=['PUT'])
@jwt_required
def change_pass():
    CURRENT_USER = current_user(get_jwt_identity())
    current_password = request.json.get("current_password")
    new_password = request.json.get("new_password")

    if bcrypt.check_password_hash(CURRENT_USER.password, current_password):
        hashed_password = bcrypt.generate_password_hash(
            new_password).decode('utf8')
        CURRENT_USER.password = hashed_password
        db.session.commit()
    else:
        return jsonify({
            "message": "Invalid credentials"
        }), 401

    return jsonify({
        "message": "Changes saved."
    }), 200


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
