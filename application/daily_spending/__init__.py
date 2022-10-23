from flask import Blueprint

daily_spending_bp = Blueprint("daily_spending_bp",__name__,template_folder="templates")

from . import views
from . import views_spending_summaries