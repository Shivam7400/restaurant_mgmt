from app.extensions import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey("tables.id"), nullable=False)

    reservation_time = db.Column(db.DateTime, nullable=False)
    guests_count = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.String(255))  # optional field
    status = db.Column(db.String(20), default="booked")  # e.g., booked, cancelled, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Reservation User {self.user_id} | Table {self.table_id} at {self.reservation_time}>"
