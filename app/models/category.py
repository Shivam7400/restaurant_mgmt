from app.extensions import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)

    items = db.relationship("Item", backref="category", cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"
