from application import db


class ShipmentUSDJPYRate(db.Model):
    __tablename__ = "shipment_usdjpy_rates"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    fx_rate = db.Column(db.Integer, nullable=False)
