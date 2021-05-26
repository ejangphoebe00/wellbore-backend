from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# instantiating db object
db = SQLAlchemy()


def create_app():
    """Construct the core application."""

    app = Flask(__name__, instance_relative_config=False)
    # The specific configuration class will depend on the value stored in the APP_SETTINGS
    # environment variable. If the variable is undefined, the configuration will fall back
    # to DevelopmentConfig by default.
    env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
    app.config.from_object(env_config)

    # Enable Cross Origin Resource Sharing 
    # (https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask)
    CORS(app)

    # database migrations
    migrate = Migrate(app, db)
    db.init_app(app)
    

    with app.app_context():
        # import models
        from .models import (CraneUser, Wellbore, WellboreCore, CoreCatalog,
                                CatalogSecurityFlag, Company, CoreType, CraneUserLoginHistory,
                                CraneWebSecurityLevel, FileFormat, FileSecurityGrade, StratLithoUnit
                                )
        return app
