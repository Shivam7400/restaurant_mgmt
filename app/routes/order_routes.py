from flask import Blueprint, request, jsonify
from app.models.order import Order, OrderItem
from app.schemas.order_schema import OrderSchema
from app.schemas.payment_schema import PaymentUpdateSchema
from app.extensions import db
from app.utils.decorators import admin_required

order_bp = Blueprint("orders", __name__, url_prefix="/orders")
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
payment_update_schema = PaymentUpdateSchema()

@order_bp.route("/", methods=["POST"])
@admin_required
def create_order():
    """
    Create a new order
    ---
    tags:
      - Orders
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - user_id
              - branch_id
              - total_amount
              - order_items
            properties:
              user_id:
                type: integer
              branch_id:
                type: integer
              total_amount:
                type: number
              order_items:
                type: array
                items:
                  type: object
                  properties:
                    item_id:
                      type: integer
                    quantity:
                      type: integer
    responses:
      201:
        description: Order created
      400:
        description: Validation error
    """
    data = request.get_json()
    errors = order_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    order = Order(
        user_id=data["user_id"],
        branch_id=data["branch_id"],
        total_amount=data["total_amount"]
    )
    db.session.add(order)
    db.session.flush()

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
@admin_required
def get_orders():
    """
    Get all orders
    ---
    tags:
      - Orders
    security:
      - BearerAuth: []
    responses:
      200:
        description: A list of orders
    """
    orders = Order.query.all()
    return jsonify(orders_schema.dump(orders)), 200

@order_bp.route("/<int:order_id>", methods=["GET"])
@admin_required
def get_order(order_id):
    """
    Get a specific order by ID
    ---
    tags:
      - Orders
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Order details
      404:
        description: Order not found
    """
    order = Order.query.get_or_404(order_id)
    return jsonify(order_schema.dump(order)), 200

@order_bp.route("/<int:order_id>", methods=["DELETE"])
@admin_required
def delete_order(order_id):
    """
    Delete an order
    ---
    tags:
      - Orders
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Order deleted
      404:
        description: Order not found
    """
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 200

@order_bp.route("/<int:order_id>/payment-status", methods=["PUT"])
@admin_required
def update_payment_status(order_id):
    """
    Update the order status
    ---
    tags:
      - Orders
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              status:
                type: string
                enum: [pending, confirmed, completed, cancelled]
    responses:
      200:
        description: Order status updated
      400:
        description: Invalid status value
      404:
        description: Order not found
    """
    data = request.get_json()
    errors = payment_update_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    payment_status = data.get("payment_status")
    payment_method = data.get("payment_method")

    order = Order.query.get_or_404(order_id)
    order.payment_status = payment_status
    if payment_method:
        order.payment_method = payment_method

    db.session.commit()
    return jsonify({
        "message": "Payment status updated",
        "order": order_schema.dump(order)
    }), 200

@order_bp.route("/<int:order_id>/status", methods=["PUT"])
@admin_required
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get("status")
    allowed_statuses = ["pending", "confirmed", "completed", "cancelled"]

    if new_status not in allowed_statuses:
        return jsonify({"error": "Invalid status value"}), 400

    order = Order.query.get_or_404(order_id)
    order.status = new_status
    db.session.commit()

    return jsonify({
        "message": "Order status updated",
        "order": order_schema.dump(order)
    }), 200