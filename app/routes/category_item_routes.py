from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.category import Category
from app.models.item import Item
from app.schemas.category_schema import CategorySchema
from app.schemas.item_schema import ItemSchema
from app.extensions import db
from app.utils.decorators import admin_required

category_bp = Blueprint("category_bp", __name__)
category_schema = CategorySchema()
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@category_bp.route("/categories/", methods=["POST"])
@jwt_required()
@admin_required
def create_category():
    data = request.get_json()
    category = Category(**data)
    db.session.add(category)
    db.session.commit()
    return category_schema.dump(category), 201

@category_bp.route("/categories/<int:category_id>/", methods=["PUT"])
@jwt_required()
@admin_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    category.name = data.get("name", category.name)
    db.session.commit()
    return category_schema.dump(category)

@category_bp.route("/categories/<int:category_id>/items/", methods=["POST"])
@jwt_required()
@admin_required
def create_item(category_id):
    data = request.get_json()
    data["category_id"] = category_id
    item = Item(**data)
    db.session.add(item)
    db.session.commit()
    return item_schema.dump(item), 201

@category_bp.route("/categories/<int:category_id>/items/", methods=["GET"])
@jwt_required()
def get_items(category_id):
    items = Item.query.filter_by(category_id=category_id).all()
    return items_schema.dump(items)
