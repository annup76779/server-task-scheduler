from datetime import timedelta
import os

import pytz

class Config(object):
    ROOT = os.path.dirname(__file__)
    APP_NAME = "scheduler"
    TESTING = False
    SECRET_KEY = '_ix8h3G_gadACQTE-mYORgv5MZY0fsOfJaqATCfDWuo'

    # Database Stuff is done here
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///main.db"
    MIGRATION_DIR = "./migrations"

    # tools dict
    TOOLS = {
        "1": "Nikto Server", "2": "Nikto Website", "3": "Zap API"
    }

    APP_EMAIL = "fypemail001@gmail.com"
    EMAIL_PASS = os.environ.get("EMAIL_PASS")


class Development(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///main.db"
    TIMEZONE = pytz.timezone("Asia/Kolkata")

class Production(Config):
    TIMEZONE = pytz.timezone("Asia/Kuala_Lumpur")

class Testing(Config):
    TESTING = True