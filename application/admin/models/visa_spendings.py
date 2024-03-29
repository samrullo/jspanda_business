from application import db


class VisaSpending(db.Model):
    __tablename__ = "visa_spending"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    visa = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
