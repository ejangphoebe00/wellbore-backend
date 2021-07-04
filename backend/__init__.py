from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
# from flask_caching import Cache

# instantiating db object
db = SQLAlchemy()
mail = Mail()



def create_app():
    """Construct the core application."""

    app = Flask(__name__, instance_relative_config=False)
    # The specific configuration class will depend on the value stored in the APP_SETTINGS
    # environment variable. If the variable is undefined, the configuration will fall back
    # to DevelopmentConfig by default.
    env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
    app.config.from_object(env_config)
    # app.config["CACHE_TYPE"] = "null"

    # Application Objects () 
    # Enable Cross Origin Resource Sharing 
    # (https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask)    
    CORS(app)
    jwt = JWTManager(app)
    mail.init_app(app)
    # database migrations
    migrate = Migrate(app, db)
    db.init_app(app)
    # cache = Cache(app)
    # cache.init_app(app)
    

    with app.app_context():
        # import models
        from .models import (CraneUser, Wellbore, WellboreCore, CoreCatalog,
                                CatalogSecurityFlag, Company, CoreType, CraneUserLoginHistory,
                                CraneWebSecurityLevel, FileFormat, FileSecurityGrade, StratLithoUnit,
                                Token
                                )

        # Import controller blueprints
        from .controllers.user import auth_bp
        from .controllers.web_security import web_security_level_bp
        from .controllers.company import company_bp
        from .controllers.welbore import wellbore_bp
        from .controllers.welbore_core import welbore_core_bp
        from .controllers.file_format import file_format_bp
        from .controllers.file_security_grade import file_security_grade_bp
        from .controllers.strat_litho_unit import strat_litho_unit_bp
        from .controllers.catalog_security_flag import catalog_security_flag_bp


        # Register Blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(web_security_level_bp)
        app.register_blueprint(company_bp)
        app.register_blueprint(wellbore_bp)
        app.register_blueprint(welbore_core_bp)
        app.register_blueprint(file_security_grade_bp)
        app.register_blueprint(file_format_bp)
        app.register_blueprint(strat_litho_unit_bp)
        app.register_blueprint(catalog_security_flag_bp)


        # revoke tokens
        @jwt.token_in_blocklist_loader
        def check_if_token_is_revoked(jwt_header, jwt_payload):
            jti = jwt_payload["jti"]
            token = db.session.query(Token.RevokedTokenModel.id).filter_by(jti=jti).scalar()
            return token is not None

        return app
