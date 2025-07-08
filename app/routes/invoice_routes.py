from flask import Blueprint, request, jsonify
from app.models.invoice import Invoice
from app.models.order import Order
from app.schemas.invoice_schema import InvoiceSchema
from app.extensions import db
from app.utils.decorators import admin_required
from datetime import datetime

invoice_bp = Blueprint("invoices", __name__, url_prefix="/invoices")
invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)

@invoice_bp.route("/<int:order_id>", methods=["POST"])
@admin_required
def generate_invoice(order_id):
    """
    Generate an invoice for a completed order
    ---
    tags:
      - Invoice
    security:
      - BearerAuth: []
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID of the completed order
    responses:
      201:
        description: Invoice generated successfully
      400:
        description: Invoice already exists or order not completed
      404:
        description: Order not found
    """
    order = Order.query.get_or_404(order_id)

    if order.status != "completed":
        return jsonify({"error": "Invoice can only be generated for completed orders"}), 400

    if order.invoice:
        return jsonify({"error": "Invoice already exists"}), 400

    invoice = Invoice(
        order_id=order.id,
        invoice_number=f"INV-{order.id}-{int(datetime.utcnow().timestamp())}",
        total_amount=order.total_amount,
        payment_status=order.payment_status
    )
    db.session.add(invoice)
    db.session.commit()

    return jsonify(invoice_schema.dump(invoice)), 201

@invoice_bp.route("/", methods=["GET"])
@admin_required
def list_invoices():
    """
    List all invoices
    ---
    tags:
      - Invoice
    security:
      - BearerAuth: []
    responses:
      200:
        description: A list of invoices
    """
    invoices = Invoice.query.all()
    return jsonify(invoices_schema.dump(invoices)), 200
