from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from functools import wraps
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"msg": "Access forbidden: Admins only"}), 403
        return fn(*args, **kwargs)
    return wrapper

def staff_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity.get("role") not in ["admin", "staff"]:
            return jsonify({"msg": "Staff access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != role:
                return jsonify({"error": "Access Forbidden"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

admin_required = role_required("admin")
staff_required = role_required("staff")
customer_required = role_required("customer")