from application import db


class ShipmentSpending(db.Model):
    __tablename__ = "shipment_spending"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
