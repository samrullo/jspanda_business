from application import db
from datetime import datetime

class JspandaOrder(db.Model):
    __tablename__ = "jspanda_orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    selling_price_per_unit = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    order_sum = db.Column(db.Float, nullable=False)
    ordered_by = db.Column(db.String(100))
    extra_notes = db.Column(db.String(400))
    is_paid = db.Column(db.Boolean, nullable=False,default=False)
    is_received = db.Column(db.Boolean, nullable=False,default=False)
    is_yubin_received = db.Column(db.Boolean, nullable=False,default=False)
    is_na_prodaju = db.Column(db.Boolean, nullable=False,default=False)
    added_time = db.Column(db.DateTime, nullable=True,default=datetime.utcnow())
    modified_time = db.Column(db.DateTime, nullable=True,default=datetime.utcnow())
