from application import db
import datetime

class SpendingCategory(db.Model):
    __tablename__="spending_categories"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    modified_at = db.Column(db.DateTime,default=datetime.datetime.utcnow)

class PaymentMethod(db.Model):
    __tablename__ = "payment_methods"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.datetime.utcnow)
    modified_at=db.Column(db.DateTime,default=datetime.datetime.utcnow)

class Spending(db.Model):
    __tablename__="spendings"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(500),nullable=False)
    spent_at=db.Column(db.DateTime,default=datetime.datetime.utcnow)
    amount=db.Column(db.Integer,nullable=False)
    spending_category_id=db.Column(db.Integer,db.ForeignKey("spending_categories.id"))
    spending_category=db.relationship("SpendingCategory",foreign_keys=[spending_category_id])
    payment_method_id=db.Column(db.Integer,db.ForeignKey("payment_methods.id"))
    payment_method=db.relationship("PaymentMethod",foreign_keys=[payment_method_id])
    receipt_image=db.Column(db.String(500))
    created_at=db.Column(db.DateTime,default=datetime.datetime.utcnow)
    modified_at=db.Column(db.DateTime,default=datetime.datetime.utcnow)

    def __str__(self) -> str:
        return f"Spending name : {self.name}, spent_at : {self.spent_at}, amount : {self.amount}, category : {self.spending_category.name}, payment_method : {self.payment_method.name}"