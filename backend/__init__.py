from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from dotenv import load_dotenv
load_dotenv()
import traceback
# from flask_caching import Cache

# instantiating db object
db = SQLAlchemy()
mail = Mail()
migrate = Migrate(compare_type=True)


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
    migrate.init_app(app, db)
    db.init_app(app)
    # cache = Cache(app)
    # cache.init_app(app)
    

    with app.app_context():
        # import models
        from .models import (Token,CraneWebSecurityLevel, CraneUser, CraneUserLoginHistory,
                                Company, Wellbore,
                                StratLithoUnit, CoreCatalog,
                                Core, Cuttings, RockSamples, FluidSamples, Files
                                )

        # Import controller blueprints
        from .controllers.web_security import web_security_level_bp
        from .controllers.user import auth_bp, create_default_user_and_security_level
        from .controllers.company import company_bp
        from .controllers.welbore import wellbore_bp
        # from .controllers.welbore_core import welbore_core_bp
        # from .controllers.file_format import file_format_bp
        # from .controllers.file_security_grade import file_security_grade_bp
        from .controllers.strat_litho_unit import strat_litho_unit_bp
        # from .controllers.catalog_security_flag import catalog_security_flag_bp
        # from .controllers.core_type import core_type_bp
        from .controllers.core_catalog import core_catalog_bp
        from .controllers.cores import core_bp
        from .controllers.cuttings import cuttings_bp
        from .controllers.rock_samples import rock_samples_bp
        from .controllers.fluid_samples import fluid_samples_bp
        from .controllers.files import files_bp
        from .controllers.dashboard import dashboard_bp





        # Register Blueprints
        app.register_blueprint(web_security_level_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(company_bp)
        app.register_blueprint(wellbore_bp)
        # app.register_blueprint(welbore_core_bp)
        # app.register_blueprint(file_security_grade_bp)
        # app.register_blueprint(file_format_bp)
        app.register_blueprint(strat_litho_unit_bp)
        # app.register_blueprint(catalog_security_flag_bp)
        # app.register_blueprint(core_type_bp)
        app.register_blueprint(core_catalog_bp)
        app.register_blueprint(core_bp)
        app.register_blueprint(cuttings_bp)
        app.register_blueprint(rock_samples_bp)
        app.register_blueprint(fluid_samples_bp)
        app.register_blueprint(files_bp)
        app.register_blueprint(dashboard_bp)


        # revoke tokens
        @jwt.token_in_blocklist_loader
        def check_if_token_is_revoked(jwt_header, jwt_payload):
            jti = jwt_payload["jti"]
            token = db.session.query(Token.RevokedTokenModel.id).filter_by(jti=jti).scalar()
            return token is not None

        # add default applciation data
        try:
            create_default_user_and_security_level()
        except:
            # print(str(traceback.format_exc()))
            print("Continue...")
            pass

        return app
