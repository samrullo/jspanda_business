from application import db


class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    pasw = db.Column(db.String(200), nullable=False)
    url = db.Column(db.Text)
    extra = db.Column(db.Text)
    date = db.Column(db.Date)

    def __repr__(self):
        return {"name": self.name, "pasw": self.pasw, "url": self.url, "extra": self.extra, "date": self.date}

    def __str__(self):
        return f"Name: {self.name}, pasw: {self.pasw}, url : {self.url}, extra : {self.extra}, date : {self.date}"
