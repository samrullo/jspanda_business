from flask import Blueprint, render_template
from flask_login import login_required
from application.jspanda_stats.controllers.jspanda_stat_controller import JspandaStatController

jspanda_stats_bp = Blueprint('jspanda_stats_bp', __name__, template_folder='templates', static_folder='static')


@jspanda_stats_bp.route("/jspanda_stats_home",methods=['GET','POST'])
@login_required
def jspanda_stats_home():
    contr = JspandaStatController()
    return contr.jspanda_stats_home()


@jspanda_stats_bp.route("/jspanda_stats/<from_date>/<to_date>", methods=['GET', 'POST'])
@login_required
def jspanda_stats_product_sales(from_date, to_date):
    contr = JspandaStatController()
    return contr.product_sales_stats(from_date, to_date)
