from application import db
from datetime import datetime

class ReceivedMoney(db.Model):
    __tablename__ = 'received_money'
    id = db.Column(db.Integer, primary_key=True)
    registered_date = db.Column(db.Date, nullable=False)
    amount_usd = db.Column(db.Integer, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    amount_jpy = db.Column(db.Integer, nullable=False)
    is_received = db.Column(db.Boolean, default=False)
    is_for_debt = db.Column(db.Boolean,default=True)
    is_allocated = db.Column(db.Boolean, default=False)    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self) -> str:
        return f"Money {self.registered_date} {self.amount_usd} usd"
