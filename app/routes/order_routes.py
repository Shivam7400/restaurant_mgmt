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

    order = Order(customer_name=data["customer_name"])
    db.session.add(order)
    db.session.flush()  # to get order.id

    for item in data["order_items"]:
        order_item = OrderItem(
            order_id=order.id,
            item_id=item["item_id"],
            quantity=item["quantity"]
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
