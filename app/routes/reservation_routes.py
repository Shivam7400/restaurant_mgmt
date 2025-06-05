from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.reservation import Reservation
from app.schemas.reservation_schema import ReservationSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.table import Table

reservation_bp = Blueprint("reservations", __name__, url_prefix="/reservations")

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)


@reservation_bp.route("/", methods=["POST"])
@jwt_required()
def create_reservation():
    data = request.get_json()
    user_id = get_jwt_identity()
    data["user_id"] = user_id

    reservation = reservation_schema.load(data)

    table = Table.query.get_or_404(reservation.table_id)
    if not table.is_available:
        return jsonify({"error": "Table is not available"}), 400
    table.is_available = False

    db.session.add(reservation)
    db.session.commit()
    return reservation_schema.jsonify(reservation), 201

@reservation_bp.route("/", methods=["GET"])
@jwt_required()
def get_reservations():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    return reservations_schema.jsonify(reservations), 200


@reservation_bp.route("/<int:reservation_id>", methods=["GET"])
@jwt_required()
def get_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    return reservation_schema.jsonify(reservation), 200

@reservation_bp.route("/<int:reservation_id>", methods=["PUT"])
@jwt_required()
def update_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    user_id = get_jwt_identity()
    if reservation.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    updated_reservation = reservation_schema.load(data, instance=reservation, partial=True)
    db.session.commit()
    return reservation_schema.jsonify(updated_reservation), 200

@reservation_bp.route("/<int:reservation_id>", methods=["DELETE"])
@jwt_required()
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    user_id = get_jwt_identity()
    if reservation.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    table = Table.query.get(reservation.table_id)
    if table:
        table.is_available = True

    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation cancelled successfully"}), 200