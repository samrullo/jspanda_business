from application import db


class Transferral(db.Model):
    __tablename__ = "transferral"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
