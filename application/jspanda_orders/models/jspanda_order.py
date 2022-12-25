from application import db
from datetime import datetime
from application.admin.models.received_money_model import ReceivedMoney

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

class JspandaOrderDebt(db.Model):
    __tablename__="jspanda_order_debts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount_usd = db.Column(db.Integer, nullable=False)    
    is_paid = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f"Debt {self.date} {self.amount_usd} usd"

class JspandaOrderDebtAllocation(db.Model):
    __tablename__="jspanda_order_debt_allocations"
    id = db.Column(db.Integer, primary_key=True)
    allocated_amount = db.Column(db.Float, nullable=False)
    jspanda_order_debt_id=db.Column(db.Integer,db.ForeignKey("jspanda_order_debts.id"))
    jspanda_order_debt=db.relationship('JspandaOrderDebt',foreign_keys=[jspanda_order_debt_id])    
    received_money_id=db.Column(db.Integer,db.ForeignKey("received_money.id"))
    received_money=db.relationship('ReceivedMoney',foreign_keys=[received_money_id])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self) -> str:
        return f"Alloc {self.created_at} {self.allocated_amount} usd"