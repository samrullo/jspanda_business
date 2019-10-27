from flask import Blueprint, render_template
from flask_login import login_required
from application.admin.controllers.received_money_controller import ReceivedMoneyController
from application.admin.controllers.shipment_spending_controller import ShipmentSpendingController
from application.admin.controllers.shipment_weight_controller import ShipmentWeightController
from application.admin.controllers.visa_spending_controller import VisaSpendingController

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/admin')


@admin_bp.route("/")
@login_required
def admin_home():
    return render_template("admin_home.html")


@admin_bp.route('/dashboard')
def admin_dashboard():
    return render_template("index.html", title="Admin dashboard")


# received money routes
@admin_bp.route('/show_received_money')
@login_required
def show_received_money():
    received_money_obj = ReceivedMoneyController()
    return received_money_obj.show_all_received_money()


@admin_bp.route("/add_received_money", methods=['GET', 'POST'])
@login_required
def add_received_money():
    contr = ReceivedMoneyController()
    return contr.add_received_money()


@admin_bp.route("/edit_received_money/<id>", methods=['GET', 'POST'])
@login_required
def edit_received_money(id):
    contr = ReceivedMoneyController()
    return contr.edit_received_money(id)


@admin_bp.route("/remove_received_money/<id>", methods=['GET', 'POST'])
@login_required
def remove_received_money(id):
    contr = ReceivedMoneyController()
    return contr.remove_received_money(id)


# routes for shipment spending
@admin_bp.route("/show_shipment_spending")
@login_required
def show_shipment_spending():
    contr = ShipmentSpendingController()
    return contr.show_all_spendings()


@admin_bp.route("/add_shipment_spending", methods=['GET', 'POST'])
@login_required
def add_shipment_spending():
    contr = ShipmentSpendingController()
    return contr.add_shipment_spending()


@admin_bp.route("/edit_shipment_spending/<id>", methods=['GET', 'POST'])
@login_required
def edit_shipment_spending(id):
    contr = ShipmentSpendingController()
    return contr.edit_shipment_spending(id)


@admin_bp.route("/remove_shipment_spending/<id>", methods=['GET', 'POST'])
@login_required
def remove_shipment_spending(id):
    contr = ShipmentSpendingController()
    return contr.remove_shipment_spending(id)


# routes for visa spending
@admin_bp.route("/show_visa_spending")
@login_required
def show_visa_spending():
    contr = VisaSpendingController()
    return contr.show_visa_spendings()


@admin_bp.route("/add_visa_spending", methods=['GET', 'POST'])
@login_required
def add_visa_spending():
    contr = VisaSpendingController()
    return contr.add_visa_spending()


@admin_bp.route("/edit_visa_spending/<id>", methods=['GET', 'POST'])
@login_required
def edit_visa_spending(id):
    contr = VisaSpendingController()
    return contr.edit_visa_spending(id)


@admin_bp.route("/remove_visa_spending/<id>", methods=['GET', 'POST'])
@login_required
def remove_visa_spending(id):
    contr = VisaSpendingController()
    return contr.remove_visa_spending(id)


# routes for shipment weights
@admin_bp.route("/show_shipment_weight")
@login_required
def show_shipment_weight():
    contr = ShipmentWeightController()
    return contr.show_pending_shipment_weights()


@admin_bp.route("/add_shipment_weight", methods=['GET', 'POST'])
@login_required
def add_shipment_weight():
    contr = ShipmentWeightController()
    return contr.add_shipment_weight()


@admin_bp.route("/edit_shipment_weight/<id>", methods=['GET', 'POST'])
@login_required
def edit_shipment_weight(id):
    contr = ShipmentWeightController()
    return contr.edit_shipment_weight(id)


@admin_bp.route("/remove_shipment_weight/<id>", methods=['GET', 'POST'])
@login_required
def remove_shipment_weight(id):
    contr = ShipmentWeightController()
    return contr.remove_shipment_weight(id)


@admin_bp.route("/mark_shipment_weight_as_paid/<id>", methods=['GET', 'POST'])
@login_required
def mark_shipment_weight_as_paid(id):
    contr = ShipmentWeightController()
    return contr.mark_as_paid(id)


@admin_bp.route("/show_all_shipment_weights")
@login_required
def show_all_shipment_weights():
    contr = ShipmentWeightController()
    return contr.show_all_shipment_weights()
