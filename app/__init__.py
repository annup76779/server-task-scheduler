from flask import Flask, current_app
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

PATH = ""

db = SQLAlchemy()
login_manager = LoginManager()
crypt = Bcrypt()
migrate = Migrate()

def create_app(config_cls = None):
    global PATH
    app  = Flask(__name__) # creating the app

    # import the custom configurations for the app
    import configmodule
    if config_cls is None:
        if app.config["ENV"] == "production":
            app.config.from_object(configmodule.Production)
        else:
            app.config.from_object(configmodule.Development)
    else:
        app.config.from_object(configmodule.Testing)
    # print(app.config)
    config_extentions(app) # getting extensions ready for the work
    config_blueprints(app) # registering the blueprint for the app
    config_errorHandler(app) # registering the error handler for the app
    
    PATH = app.config["ROOT"]
    return app


def config_extentions(app):
    
    db.init_app(app) # SQLAlchemy
    migrate.init_app(app, db) # Database migrate
    crypt.init_app(app) # Bcrypt
    login_manager.init_app(app, db) # LoginManager

    login_manager.login_message = "Please login to use this page."
    login_manager.login_view = "user.login"
    login_manager.session_protection = "strong"
    login_manager.login_message_category = "info"

    from app.model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


def config_blueprints(app):
    from app.user import user_bp
    app.register_blueprint(user_bp)
    os.makedirs(name = os.path.join(PATH, user_bp.static_folder), exist_ok = True)

    from app.general import api
    app.register_blueprint(api)
    os.makedirs(name = os.path.join(PATH, api.static_folder), exist_ok = True)

def config_errorHandler(app):
    pass