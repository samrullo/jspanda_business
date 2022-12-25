from flask import Blueprint

jspanda_orders_bp = Blueprint('jspanda_orders_bp', __name__, template_folder='templates', static_folder='static')
from flask import render_template
from flask_login import login_required
from . import jspanda_orders_routes
from . import jspanda_order_debt_views
from . import debt_allocation_views