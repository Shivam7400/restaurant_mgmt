from flask import Blueprint, request, jsonify
from app.models.staff import Staff
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from app.schemas.staff_schema import StaffSchema
from app.utils.decorators import admin_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

staff_schema = StaffSchema()

@auth_bp.route("/register", methods=["POST"])
@admin_required
def register():
    data = request.get_json()
    errors = staff_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    if Staff.query.filter((Staff.username == data["username"]) | (Staff.email == data["email"])).first():
        return jsonify({"msg": "Username or Email already exists"}), 409

    staff = Staff(
        username=data["username"],
        email=data["email"],
        role=data.get("role", "staff")
    )
    staff.set_password(data["password"])
    db.session.add(staff)
    db.session.commit()

    return jsonify(staff_schema.dump(staff)), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"msg": "Username and password required"}), 400

    staff = Staff.query.filter_by(username=data["username"]).first()
    if not staff or not staff.check_password(data["password"]):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(
        identity=str(staff.id),
        additional_claims={"username": staff.username, "role": staff.role}
    )
    return jsonify({"access_token": access_token, "user": {"id": staff.id, "username": staff.username, "role": staff.role}}), 200

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    jwt_data = get_jwt()
    return {"msg": f"Hello {jwt_data['username']}! You are a {jwt_data['role']}"}, 200

@auth_bp.route("/admin-only", methods=["GET"])
@admin_required
def admin_only():
    return {"msg": "Welcome Admin! This is a restricted route."}, 200