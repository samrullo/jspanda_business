from flask import Blueprint

db_admin_bp = Blueprint('db_admin_bp', __name__)

from . import views
