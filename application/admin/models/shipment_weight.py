from application import db


class ShipmentWeight(db.Model):
    __tablename__ = "shipment_weight"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    to_whom = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    is_paid = db.Column(db.Boolean)
    order_date = db.Column(db.Date, nullable=True)
