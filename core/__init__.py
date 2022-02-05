from distutils.command.config import config
from flask import Flask
from flask.json import jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger
from flask_migrate import Migrate

app = Flask(__name__)
cors = CORS(app, 
            headers=['Content-Type'],
            expose_headers=['Access-Control-Allow-Origin'],
            supports_credentials=True)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
    cors.orgins = ["https://www.reminderse.com"]
elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")
    cors.origins = ["http://localhost:3000"]
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
    cors.origins = ["https://.*--vigorous-varahamihira-d00b87.netlify.app"]

db = SQLAlchemy(app, engine_options={'pool_pre_ping': True})
db.create_all()
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
login_manager.session_protection = 'none'
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
jwt = JWTManager(app)
print(app.config)

version = "0.0.1"
build = app.config["HEROKU_BUILD"]
from core.users.routes import users
from core.entries.routes import entries

app.register_blueprint(users)
app.register_blueprint(entries)
app.register_blueprint(get_swaggerui_blueprint(
    app.config["SWAGGER_URL"],
    app.config["API_URL"],
    config={
        'app_name': 'Reminderse API'
    }
))