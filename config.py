from os import environ
import pyodbc
from datetime import timedelta

class Config(object):
    """ app configuration class """
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:Boeing747@@localhost:1433/WellBoreStoreDB?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # jwt configuarations for the user auth api
    JWT_SECRET_KEY = environ.get('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

class DevelopmentConfig(Config):
    """ app development configuration class """
    ENV = "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
