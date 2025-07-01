from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models.staff import Staff
from app.schemas.staff_schema import StaffSchema
from app.extensions import db
from app.utils.decorators import admin_required
from app.extensions import blacklist

staff_schema = StaffSchema()
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
staffs_schema = StaffSchema(many=True)

@auth_bp.route("/register", methods=["POST"])
@jwt_required() # Ensure only admins can register new staff
@admin_required # Custom decorator to check if the user is an admin
def register():
    """
    Register a new staff user
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
            role:
              type: string
              enum: [admin, staff, customer]
    responses:
      201:
        description: Staff registered successfully
      400:
        description: Validation error
      409:
        description: Username or Email already exists
    """
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
    """
    Staff login and receive JWT token
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Successful login
      400:
        description: Missing username or password
      401:
        description: Invalid credentials
    """
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
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": staff.id,
            "username": staff.username,
            "role": staff.role
        }
    }), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    Get current logged-in user details
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Current user info
    """
    jwt_data = get_jwt()
    return jsonify({
        "username": jwt_data["username"],
        "role": jwt_data["role"]
    }), 200

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Protected route example
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Success message
    """
    jwt_data = get_jwt()
    return jsonify({"msg": f"Hello {jwt_data['username']}! You are a {jwt_data['role']}"}), 200

@auth_bp.route("/admin-only", methods=["GET"])
@admin_required
def admin_only():
    """
    Admin-only route
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Admin access granted
      403:
        description: Access forbidden for non-admins
    """
    return jsonify({"msg": "Welcome Admin! This is a restricted route."}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Logout user (JWT revocation logic to be implemented)
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: User logged out
    """
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200