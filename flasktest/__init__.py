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

app = Flask(__name__)
# CORS(app, resources={r'/*': {"origins": ["https://localhost:3000",
#                                          "https://reminderse.com"]}}, supports_credentials=True)
# CORS(app, resources={r'/api/*': {
#     "origins":  ["https://618ec617dcd64c000799a047--vigorous-varahamihira-d00b87.netlify.app"]
#     }}, supports_credentials=True)
cors = CORS(app, origins=["https://61eaeb755caa0000072e645d--vigorous-varahamihira-d00b87.netlify.app/",
                          "https://www.reminderse.com"
                          ],
            headers=['Content-Type'],
            expose_headers=['Access-Control-Allow-Origin'],
            supports_credentials=True)
# CORS(app, supports_credentials=True)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")

db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
login_manager.session_protection = 'none'
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
jwt = JWTManager(app)
print(app.config)

version = "0.0.1"
build = app.config["HEROKU_BUILD"]
from flasktest.users.routes import users
from flasktest.entries.routes import entries

app.register_blueprint(users)
app.register_blueprint(entries)
app.register_blueprint(get_swaggerui_blueprint(
    app.config["SWAGGER_URL"],
    app.config["API_URL"],
    config={
        'app_name': 'Reminderse API'
    }
))