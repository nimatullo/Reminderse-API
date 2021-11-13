import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    HEROKU_BUILD = os.environ.get('HEROKU_RELEASE_VERSION')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAIL_SERVER = 'smtp.zoho.com'
    MAIL_SERVER_ID = os.environ.get("MAIL_SERVER_ID")
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # REMEMBER_COOKIE_DURATION = timedelta(days=7)
    # REMEMBER_COOKIE_SECURE = True
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    JWT_CSRF_IN_COOKIES = True
    JWT_COOKIE_SAMESITE = None
    # JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = False


class DevelopmentConfig(Config):
    SECRET_KEY = "NIMATULLO_SECRET"
    MAIL_SERVER_ID = "zoho"
    MAIL_API_KEY = "abcefghij"
    MAIL_PASSWORD = "password"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://puffer:puffer@localhost:5432/reminderse"
    HEROKU_BUILD  = "local"
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'


class TestingConfig(Config):
    TESTING = True
    HEROKU_BUILD = os.environ.get('HEROKU_RELEASE_VERSION')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAIL_SERVER = 'smtp.zoho.com'
    MAIL_SERVER_ID = os.environ.get("MAIL_SERVER_ID")
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # REMEMBER_COOKIE_DURATION = timedelta(days=7)
    # REMEMBER_COOKIE_SECURE = True
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    JWT_CSRF_IN_COOKIES = True
    JWT_COOKIE_SAMESITE = None
    # JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = False
