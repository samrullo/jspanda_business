from application import db


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
    ordered_by = db.Column(db.String(100), nullable=True)
    extra_notes = db.Column(db.String(400), nullable=True)
    is_paid = db.Column(db.Boolean, nullable=False)
    added_time = db.Column(db.DateTime, nullable=True)
    modified_time = db.Column(db.DateTime, nullable=True)
