from flask import Blueprint
from flask import current_app

mortgage_app_bp = Blueprint("mortgage_app_bp",__name__,url_prefix="/mortgage",template_folder=str(current_app.config["REACT_MORTGAGE_APP_FOLDER"]),static_folder=str(current_app.config["REACT_MORTGAGE_APP_FOLDER"]/"static"))

from . import views
