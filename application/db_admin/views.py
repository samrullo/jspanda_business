from application import db, admin_flask

from application.db_admin.model_views import ShipmentPriceView,FamilySpendingView,SpendingCategoryView,PaymentMethodView
from application.admin.models.shipment_weight import ShipmentPrice
from application.admin.models.family_spending import FamilySpending

from application.db_admin.model_views import ShipmentUSDJPYRateView
from application.admin.models.shipment_usdjpy_rate import ShipmentUSDJPYRate

from application.db_admin.model_views import ShipmentPriceUSDView
from application.admin.models.shipment_weight import ShipmentPriceUSD
from application.daily_spending.models import SpendingCategory,PaymentMethod

admin_flask.add_view(ShipmentPriceView(ShipmentPrice, db.session))
admin_flask.add_view(ShipmentPriceUSDView(ShipmentPriceUSD, db.session))
admin_flask.add_view(ShipmentUSDJPYRateView(ShipmentUSDJPYRate,db.session))
admin_flask.add_view(FamilySpendingView(FamilySpending,db.session))

admin_flask.add_view(SpendingCategoryView(SpendingCategory,db.session))
admin_flask.add_view(PaymentMethodView(PaymentMethod,db.session))