from app.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id"), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pending")
    payment_status = db.Column(db.String(20), default="unpaid") 
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")
    invoice = db.relationship("Invoice", backref="order", uselist=False)

    def __repr__(self):
        return f"<Order {self.id} | Total {self.total_amount}>"
