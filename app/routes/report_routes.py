from flask import Blueprint, jsonify
from app.models.order import Order
from app.extensions import db
from datetime import date
from sqlalchemy import func

report_bp = Blueprint("reports", __name__, url_prefix="/reports")

@report_bp.route("/daily-sales", methods=["GET"])
def daily_sales_report():
    """
    Get daily sales report
    ---
    tags:
      - Reports
    summary: Daily Sales Report
    description: Returns the total number of orders and total revenue for today.
    responses:
      200:
        description: Sales report for the current day
        schema:
          type: object
          properties:
            date:
              type: string
              format: date
              example: "2025-06-23"
            total_orders:
              type: integer
              example: 15
            total_revenue:
              type: number
              format: float
              example: 12345.67
    """
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
