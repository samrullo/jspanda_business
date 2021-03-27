from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class ShipmentPriceView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_active and current_user.is_admin

class FamilySpendingView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_active and current_user.is_admin
