from application import db


class FamilySpending(db.Model):
    __tablename__ = "family_spending"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer, nullable=False)