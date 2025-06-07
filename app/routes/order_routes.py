from flask import Blueprint, request, jsonify
from app.models.order import Order, OrderItem
from app.schemas.order_schema import OrderSchema
from app.extensions import db
from app.utils.decorators import admin_required

order_bp = Blueprint("orders", __name__, url_prefix="/orders")
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@order_bp.route("/", methods=["POST"])
@admin_required
def create_order():
    data = request.get_json()
    errors = order_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    order = Order(
        user_id=data["user_id"],
        branch_id=data["branch_id"],
        total_amount=data["total_amount"],
        status="pending"
    )
    db.session.add(order)
    db.session.flush()

    for item in data["order_items"]:
        order_item = OrderItem(
            order_id=order.id,
            item_id=item["item_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            total_price=item["unit_price"] * item["quantity"]
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify(order_schema.dump(order)), 201

@order_bp.route("/", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify(orders_schema.dump(orders)), 200

@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order_schema.dump(order)), 200

@order_bp.route("/<int:order_id>", methods=["DELETE"])
@admin_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 200

@order_bp.route("/<int:order_id>/status", methods=["PUT"])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ["pending", "confirmed", "completed", "cancelled"]:
        return jsonify({"error": "Invalid status"}), 400

    order.status = new_status
    db.session.commit()
    return jsonify(order_schema.dump(order)), 200

@order_bp.route("/user/<int:user_id>", methods=["GET"])
def get_orders_by_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify(orders_schema.dump(orders)), 200