from flasktest.entries.routes import entries
from flasktest.users.routes import users
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer

from flasktest.config import Config

version = "0.1.2"

app = Flask(__name__)
# CORS(app, resources={r'/*': {"origins": ["https://localhost:3000",
#                                          "https://reminderse.com"]}}, supports_credentials=True)
CORS(app, supports_credentials=True)
app.config.from_object(Config)
print(Config)
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
login_manager.session_protection = 'none'
ts = URLSafeTimedSerializer(Config.SECRET_KEY)
jwt = JWTManager(app)


app.register_blueprint(users)
app.register_blueprint(entries)
