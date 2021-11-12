import subprocess
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer



app = Flask(__name__)
# CORS(app, resources={r'/*': {"origins": ["https://localhost:3000",
#                                          "https://reminderse.com"]}}, supports_credentials=True)
CORS(app, supports_credentials=True)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")


version = "0.1.3"
build = app.config["HEROKU_RELEASE_VERSION"]

db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
login_manager.session_protection = 'none'
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
jwt = JWTManager(app)


from flasktest.users.routes import users
from flasktest.entries.routes import entries
app.register_blueprint(users)
app.register_blueprint(entries)
