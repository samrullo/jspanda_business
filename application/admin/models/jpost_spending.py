from application import db


class JpostSpending(db.Model):
    __tablename__ = "jpost_spending"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
