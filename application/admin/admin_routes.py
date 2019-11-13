from flask import Blueprint, render_template
from flask_login import login_required
from application.admin.controllers.received_money_controller import ReceivedMoneyController
from application.admin.controllers.shipment_spending_controller import ShipmentSpendingController
from application.admin.controllers.jpost_controller import JpostSpendingController
from application.admin.controllers.shipment_weight_controller import ShipmentWeightController
from application.admin.controllers.visa_spending_controller import VisaSpendingController
from application.admin.controllers.transferral_controller import TransferralController
from application.admin.controllers.family_spending_controller import FamilySpendingController
from application.admin.controllers.summary_controller import SummaryController

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/admin')


@admin_bp.route("/")
@login_required
def admin_home():
    return render_template("admin_home.html")


@admin_bp.route('/dashboard')
def admin_dashboard():
    return render_template("index.html", title="Admin dashboard")


# show summary of income and spendings
@admin_bp.route("/show_summary")
@login_required
def show_summary():
    contr = SummaryController()
    return contr.show_summary()


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


# routes for yubin spendings
@admin_bp.route("/show_jpost_spending")
@login_required
def show_jpost_spending():
    contr = JpostSpendingController()
    return contr.show_all_spendings()


@admin_bp.route("/add_jpost_spending", methods=['GET', 'POST'])
@login_required
def add_jpost_spending():
    contr = JpostSpendingController()
    return contr.add_jpost_spending()


@admin_bp.route("/edit_jpost_spending/<id>", methods=['GET', 'POST'])
@login_required
def edit_jpost_spending(id):
    contr = JpostSpendingController()
    return contr.edit_jpost_spending(id)


@admin_bp.route("/remove_jpost_spending/<id>", methods=['GET', 'POST'])
@login_required
def remove_jpost_spending(id):
    contr = JpostSpendingController()
    return contr.remove_jpost_spending(id)


# routes for visa spending
@admin_bp.route("/show_visa_spending")
@login_required
def show_visa_spending():
    contr = VisaSpendingController()
    return contr.show_visa_spendings()


@admin_bp.route("/show_visa_spending_by_date/<date>")
@login_required
def show_visa_spending_by_date(date):
    contr = VisaSpendingController()
    return contr.show_visa_spendings_by_date(date)


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


# routes for transferrals
@admin_bp.route("/show_transferrals")
@login_required
def show_transferrals():
    contr = TransferralController()
    return contr.show_transferrals()


@admin_bp.route("/add_transferral", methods=['GET', 'POST'])
@login_required
def add_transferral():
    contr = TransferralController()
    return contr.add_transferral()


@admin_bp.route("/edit_transferral/<id>", methods=['GET', 'POST'])
@login_required
def edit_transferral(id):
    contr = TransferralController()
    return contr.edit_transferral(id)


@admin_bp.route("/remove_transferral/<id>", methods=['GET', 'POST'])
@login_required
def remove_transferral(id):
    contr = TransferralController()
    return contr.remove_transferral(id)


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


@admin_bp.route("/show_shipment_weights_by_date")
@login_required
def show_shipment_weights_by_date():
    contr = ShipmentWeightController()
    return contr.show_shipment_weights_by_date()


# family spending routes
@admin_bp.route("/family_spending_main")
@login_required
def family_spending_main():
    contr = FamilySpendingController()
    return contr.family_spending_main()


@admin_bp.route("/family_spending_by_month/<adate>")
@login_required
def family_spending_by_month(adate):
    contr = FamilySpendingController()
    return contr.family_spending_month(adate)


@admin_bp.route("/add_family_spending", methods=['GET', 'POST'])
@login_required
def add_family_spending():
    contr = FamilySpendingController()
    return contr.add_family_spending()


@admin_bp.route("/edit_family_spending/<id>", methods=['GET', 'POST'])
@login_required
def edit_family_spending(id):
    contr = FamilySpendingController()
    return contr.edit_family_spending(id)


@admin_bp.route("/remove_family_spending", methods=['GET', 'POST'])
@login_required
def remove_family_spending(id):
    contr = FamilySpendingController()
    return contr.remove_family_spending(id)
