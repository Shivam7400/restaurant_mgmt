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
    """
    Create a new branch
    ---
    tags:
      - Branch
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - address
            - city
            - restaurant_id
          properties:
            address:
              type: string
            city:
              type: string
            restaurant_id:
              type: integer
    responses:
      201:
        description: Branch created successfully
      400:
        description: Validation error
    """
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
    """
    Get all branches
    ---
    tags:
      - Branch
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of branches
    """
    branches = Branch.query.all()
    return jsonify(branches_schema.dump(branches)), 200

@branch_bp.route("/<int:branch_id>", methods=["GET"])
@jwt_required()
def get_branch(branch_id):
    """
    Get a single branch by ID
    ---
    tags:
      - Branch
    security:
      - BearerAuth: []
    parameters:
      - name: branch_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Branch data
      404:
        description: Branch not found
    """
    branch = Branch.query.get_or_404(branch_id)
    return jsonify(branch_schema.dump(branch)), 200

@branch_bp.route("/<int:branch_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_branch(branch_id):
    """
    Update an existing branch
    ---
    tags:
      - Branch
    security:
      - BearerAuth: []
    parameters:
      - name: branch_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            address:
              type: string
            city:
              type: string
            restaurant_id:
              type: integer
    responses:
      200:
        description: Branch updated
      400:
        description: Validation error
      404:
        description: Branch not found
    """
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
    """
    Delete a branch
    ---
    tags:
      - Branch
    security:
      - BearerAuth: []
    parameters:
      - name: branch_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Branch deleted successfully
      404:
        description: Branch not found
    """
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    return jsonify({"msg": "Branch deleted successfully"}), 200
