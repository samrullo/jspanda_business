from flask import Blueprint, render_template
from flask_login import login_required
from application.admin.controllers.received_money_controller import ReceivedMoneyController
from application.admin.controllers.shipment_spending_controller import ShipmentSpendingController
from application.admin.controllers.shipment_weight_controller import ShipmentWeightController
from application.admin.controllers.visa_spending_controller import VisaSpendingController
from application.admin.controllers.family_spending_controller import FamilySpendingController
from application.jspanda_orders.controllers.jspanda_orders_controllers import JspandaOrderController

jspanda_orders_bp = Blueprint('jspanda_orders_bp', __name__, template_folder='templates', static_folder='static')


@jspanda_orders_bp.route("/jspanda_orders")
@login_required
def jspanda_orders():
    contr = JspandaOrderController()
    return contr.show_jspanda_orders()


@jspanda_orders_bp.route("/jspanda_orders_by_date/<adate>")
@login_required
def jspanda_orders_by_date(adate):
    contr = JspandaOrderController()
    return contr.show_jspanda_orders_by_date(adate)


@jspanda_orders_bp.route("/add_jspanda_order", methods=['GET', 'POST'])
@login_required
def add_jspanda_order():
    contr = JspandaOrderController()
    return contr.add_jspanda_order()
