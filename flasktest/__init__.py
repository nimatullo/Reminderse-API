from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flasktest.config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
# CORS(app, resources={r'/*': {"origins": ["https://localhost:3000",
#                                          "https://reminderse.com"]}}, supports_credentials=True)
CORS(app, supports_credentials=True)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
login_manager.session_protection = 'none'
ts = URLSafeTimedSerializer(Config.SECRET_KEY)
jwt = JWTManager(app)


from flasktest.users.routes import users
from flasktest.entries.routes import entries
app.register_blueprint(users)
app.register_blueprint(entries)
