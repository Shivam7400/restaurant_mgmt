from flask import Blueprint, request, jsonify
from app.models.branch import Branch
from app.extensions import db
from app.schemas.branch_schema import BranchSchema
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required

branch_bp = Blueprint("branches", __name__, url_prefix="/branches")
branch_schema = BranchSchema()
branches_schema = BranchSchema(many=True)

@branch_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_branch():
    data = request.get_json()
    errors = branch_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    branch = Branch(
        address=data["address"],
        city=data["city"],
        restaurant_id=data["restaurant_id"]
    )
    db.session.add(branch)
    db.session.commit()
    return jsonify(branch_schema.dump(branch)), 201

@branch_bp.route("/", methods=["GET"])
@jwt_required()
def get_branches():
    branches = Branch.query.all()
    return jsonify(branches_schema.dump(branches)), 200

@branch_bp.route("/<int:branch_id>", methods=["GET"])
@jwt_required()
def get_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    return jsonify(branch_schema.dump(branch)), 200

@branch_bp.route("/<int:branch_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    data = request.get_json()
    errors = branch_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    branch.address = data["address"]
    branch.city = data["city"]
    branch.restaurant_id = data["restaurant_id"]
    db.session.commit()
    return jsonify(branch_schema.dump(branch)), 200

@branch_bp.route("/<int:branch_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    return jsonify({"msg": "Branch deleted successfully"}), 200
