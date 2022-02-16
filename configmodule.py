from datetime import timedelta
import os

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


class Development(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///main.db"

class Production(Config):
    pass

class Testing(Config):
    TESTING = True