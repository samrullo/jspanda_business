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
from application.admin.controllers.account_controller import AccountController
from application.jspanda_tests.controllers.flask_upload_test_controller import FlaskUploadTestController

jspanda_test_bp = Blueprint('jspanda_test_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/jspanda_test')


@jspanda_test_bp.route("/", methods=['GET', 'POST'])
def jspanda_test_home():
    contr = FlaskUploadTestController()
    return contr.upload()
