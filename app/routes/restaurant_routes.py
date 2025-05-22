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
    restaurants = Restaurant.query.all()
    return restaurant_list_schema.dump(restaurants), 200

@restaurant_bp.route("/<int:restaurant_id>/branches", methods=["POST"])
@jwt_required()
@admin_required
def create_branch(restaurant_id):
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
    branches = Branch.query.filter_by(restaurant_id=restaurant_id).all()
    return branch_list_schema.dump(branches), 200
