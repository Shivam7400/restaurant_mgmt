from flask import Blueprint, request, jsonify
from app.models.restaurant import Restaurant
from app.models.branch import Branch
from app.schemas.restaurant_schema import RestaurantSchema
from app.schemas.branch_schema import BranchSchema
from app.extensions import db
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required

restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/restaurants")

restaurant_schema = RestaurantSchema()
branch_schema = BranchSchema()
restaurant_list_schema = RestaurantSchema(many=True)
branch_list_schema = BranchSchema(many=True)

@restaurant_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_restaurant():
    """
    Create a new restaurant
    ---
    tags:
      - Restaurants
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - location
            - contact_number
          properties:
            name:
              type: string
              example: "Shivam's Diner"
            location:
              type: string
              example: "Delhi, India"
            contact_number:
              type: string
              example: "+91-9999999999"
    responses:
      201:
        description: Restaurant created successfully
      400:
        description: Validation error
    """
    data = request.get_json()
    errors = restaurant_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    restaurant = Restaurant(**data)
    db.session.add(restaurant)
    db.session.commit()
    return restaurant_schema.dump(restaurant), 201


@restaurant_bp.route("/", methods=["GET"])
@jwt_required()
def get_restaurants():
    """
    Get all restaurants
    ---
    tags:
      - Restaurants
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of restaurants
        schema:
          type: array
          items:
            $ref: '#/definitions/Restaurant'
    """
    restaurants = Restaurant.query.all()
    return restaurant_list_schema.dump(restaurants), 200


@restaurant_bp.route("/<int:restaurant_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_restaurant(restaurant_id):
    """
    Update a restaurant
    ---
    tags:
      - Restaurants
    security:
      - BearerAuth: []
    parameters:
      - name: restaurant_id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Restaurant'
    responses:
      200:
        description: Restaurant updated successfully
        schema:
          $ref: '#/definitions/Restaurant'
      404:
        description: Restaurant not found
    """
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    data = request.get_json()
    restaurant.name = data.get("name", restaurant.name)
    restaurant.description = data.get("description", restaurant.description)
    db.session.commit()
    return restaurant_schema.dump(restaurant), 200


@restaurant_bp.route("/<int:restaurant_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_restaurant(restaurant_id):
    """
    Delete a restaurant (only if it has no branches)
    ---
    tags:
      - Restaurants
    security:
      - BearerAuth: []
    parameters:
      - name: restaurant_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Restaurant deleted successfully
      400:
        description: Cannot delete restaurant with existing branches
      404:
        description: Restaurant not found
    """
    restaurant = Restaurant.query.get_or_404(restaurant_id)

    # Check if any branches exist for this restaurant
    if Branch.query.filter_by(restaurant_id=restaurant.id).first():
        return jsonify({"error": "Cannot delete restaurant with existing branches"}), 400

    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({"message": "Restaurant deleted successfully"}), 200


@restaurant_bp.route("/<int:restaurant_id>/branches", methods=["POST"])
@jwt_required()
@admin_required
def create_branch(restaurant_id):
    """
    Create a branch for a restaurant
    ---
    tags:
      - Branches
    security:
      - BearerAuth: []
    parameters:
      - name: restaurant_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Branch'
    responses:
      201:
        description: Branch created
        schema:
          $ref: '#/definitions/Branch'
      400:
        description: Validation error
    """
    data = request.get_json()
    data["restaurant_id"] = restaurant_id
    errors = branch_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    branch = Branch(**data)
    db.session.add(branch)
    db.session.commit()
    return branch_schema.dump(branch), 201


@restaurant_bp.route("/<int:restaurant_id>/branches", methods=["GET"])
@jwt_required()
def get_branches(restaurant_id):
    """
    Get branches of a specific restaurant
    ---
    tags:
      - Branches
    security:
      - BearerAuth: []
    parameters:
      - name: restaurant_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: List of branches
        schema:
          type: array
          items:
            $ref: '#/definitions/Branch'
    """
    branches = Branch.query.filter_by(restaurant_id=restaurant_id).all()
    return branch_list_schema.dump(branches), 200


@restaurant_bp.route("/<int:restaurant_id>/branches/<int:branch_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_branch(restaurant_id, branch_id):
    """
    Update a branch of a restaurant
    ---
    tags:
      - Branches
    security:
      - BearerAuth: []
    parameters:
      - name: restaurant_id
        in: path
        required: true
        type: integer
      - name: branch_id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Branch'
    responses:
      200:
        description: Branch updated
        schema:
          $ref: '#/definitions/Branch'
      404:
        description: Branch not found
    """
    branch = Branch.query.get_or_404(branch_id)
    data = request.get_json()
    branch.address = data.get("address", branch.address)
    branch.city = data.get("city", branch.city)
    db.session.commit()
    return branch_schema.dump(branch), 200


@restaurant_bp.route("/<int:restaurant_id>/branches/<int:branch_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_branch(restaurant_id, branch_id):
    """
    Delete a branch of a restaurant
    ---
    tags:
      - Branches
    security:
      - BearerAuth: []
    parameters:
      - name: restaurant_id
        in: path
        required: true
        type: integer
      - name: branch_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Branch deleted
      404:
        description: Branch not found
    """
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    return jsonify({"message": "Branch deleted successfully"}), 200
