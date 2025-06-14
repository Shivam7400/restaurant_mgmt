from flask import Blueprint, jsonify
from app.models.order import Order
from app.extensions import db
from datetime import date
from sqlalchemy import func

report_bp = Blueprint("reports", __name__, url_prefix="/reports")

@report_bp.route("/daily-sales", methods=["GET"])
def daily_sales_report():
    today = date.today()
    orders_today = (
        db.session.query(func.count(Order.id), func.sum(Order.total_amount))
        .filter(func.date(Order.created_at) == today)
        .first()
    )

    return jsonify({
        "date": today.isoformat(),
        "total_orders": orders_today[0] or 0,
        "total_revenue": float(orders_today[1]) if orders_today[1] else 0.0
    }), 200
