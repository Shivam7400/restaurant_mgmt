from app.extensions import db

class Table(db.Model):
    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(10), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(100))  # e.g., Window, Outdoor, etc.
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id"), nullable=False)

    def __repr__(self):
        return f"<Table {self.table_number} - {self.seats} seats>"
