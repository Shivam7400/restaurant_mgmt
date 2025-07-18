from app.extensions import db

class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    location = db.Column(db.String(150), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    branches = db.relationship("Branch", backref="restaurant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Restaurant {self.name}>"
