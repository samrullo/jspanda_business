from application import db


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"{self.name}"
