from app.extensions import db

class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)

    def __repr__(self):
        return f"<Menu {self.name} - ${self.price}>"
