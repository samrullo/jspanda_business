from application import db, admin_flask

from application.db_admin.model_views import ShipmentPriceView,FamilySpendingView
from application.admin.models.shipment_weight import ShipmentPrice
from application.admin.models.family_spending import FamilySpending

admin_flask.add_view(ShipmentPriceView(ShipmentPrice, db.session))
admin_flask.add_view(FamilySpendingView(FamilySpending,db.session))
