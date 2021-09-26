from os import environ
import pyodbc
from datetime import timedelta

class Config(object):
    """ app configuration class """
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = (environ.get('SQLALCHEMY_DATABASE_URI'))
    # SQLALCHEMY_DATABASE_URI="mssql+pyodbc://<user>:<password>@<server>/<database_name>?driver=<database_driver>"
    USER = environ.get('DB_USER')
    PASSWORD = environ.get('DB_PASSWORD')
    DB_NAME = environ.get('DB_NAME')
    HOST = environ.get('DB_HOST')
    
    SQLALCHEMY_DATABASE_URI=f"mssql+pyodbc://{USER}:{PASSWORD}@{HOST}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # jwt configuarations for the user auth api
    JWT_SECRET_KEY = environ.get('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    # email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = str(environ.get('MAIL_PASSWORD'))
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    # print(environ.get('MAIL_PASSWORD'))

class DevelopmentConfig(Config):
    """ app development configuration class """
    ENV = "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
