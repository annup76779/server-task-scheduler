from flask import Blueprint

api = Blueprint('api', __name__, url_prefix="/api", static_folder="../static/output")

from app.general import routes