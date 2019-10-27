from application import db


class ReceivedMoney(db.Model):
    __tablename__ = 'received_money'
    id = db.Column(db.Integer, primary_key=True)
    registered_date = db.Column(db.Date, nullable=False)
    amount_usd = db.Column(db.Integer, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    amount_jpy = db.Column(db.Integer, nullable=False)
