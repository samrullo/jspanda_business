from flask import Blueprint, render_template
from flask_login import login_required
from application.admin.controllers.received_money_controller import ReceivedMoneyController
from application.admin.controllers.shipment_spending_controller import ShipmentSpendingController
from application.admin.controllers.shipment_weight_controller import ShipmentWeightController
from application.admin.controllers.visa_spending_controller import VisaSpendingController
from application.admin.controllers.family_spending_controller import FamilySpendingController

jspanda_orders_bp = Blueprint('jspanda_orders_bp', __name__, template_folder='templates', static_folder='static')


@jspanda_orders_bp.route("/jspanda_orders")
@login_required
def jspanda_orders():
    return render_template("jspanda_orders.html", title="JSPanda orders")
