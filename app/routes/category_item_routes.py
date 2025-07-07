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
categories_schema = CategorySchema(many=True)
items_schema = ItemSchema(many=True)

@category_bp.route("/categories/", methods=["POST"])
@jwt_required()
@admin_required
def create_category():
    """
    Create a new category
    ---
    tags:
      - Category
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: category
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
    responses:
      201:
        description: Category created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    category = Category(**data)
    db.session.add(category)
    db.session.commit()
    return category_schema.dump(category), 201


@category_bp.route("/categories/", methods=["GET"])
@jwt_required()
def get_categories():
    """
    Get all categories
    ---
    tags:
      - Category
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of categories
    """
    categories = Category.query.all()
    return categories_schema.dump(categories), 200


@category_bp.route("/categories/<int:category_id>/", methods=["PUT"])
@jwt_required()
@admin_required
def update_category(category_id):
    """
    Update a category by ID
    ---
    tags:
      - Category
    security:
      - BearerAuth: []
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
      - in: body
        name: category
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
    responses:
      200:
        description: Category updated successfully
      404:
        description: Category not found
    """
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    category.name = data.get("name", category.name)
    db.session.commit()
    return category_schema.dump(category), 200


@category_bp.route("/categories/<int:category_id>/", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_category(category_id):
    """
    Delete a category if it has no items
    ---
    tags:
      - Category
    security:
      - BearerAuth: []
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Category deleted successfully
      400:
        description: Cannot delete category with items
    """
    category = Category.query.get_or_404(category_id)
    items = Item.query.filter_by(category_id=category_id).first()
    if items:
        return jsonify({"error": "Cannot delete category with items"}), 400

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200


@category_bp.route("/categories/<int:category_id>/items/", methods=["POST"])
@jwt_required()
@admin_required
def create_item(category_id):
    """
    Create a new item under a category
    ---
    tags:
      - Item
    security:
      - BearerAuth: []
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
      - in: body
        name: item
        required: true
        schema:
          type: object
          required:
            - name
            - price
          properties:
            name:
              type: string
            description:
              type: string
            price:
              type: number
    responses:
      201:
        description: Item created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    data["category_id"] = category_id
    item = Item(**data)
    db.session.add(item)
    db.session.commit()
    return item_schema.dump(item), 201


@category_bp.route("/categories/<int:category_id>/items/", methods=["GET"])
@jwt_required()
def get_items(category_id):
    """
    Get all items under a category
    ---
    tags:
      - Item
    security:
      - BearerAuth: []
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: List of items
      404:
        description: Category not found
    """
    items = Item.query.filter_by(category_id=category_id).all()
    return items_schema.dump(items), 200


@category_bp.route("/categories/<int:category_id>/items/<int:item_id>/", methods=["PUT"])
@jwt_required()
@admin_required
def update_item(category_id, item_id):
    """
    Update an item under a category
    ---
    tags:
      - Item
    security:
      - BearerAuth: []
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
      - name: item_id
        in: path
        type: integer
        required: true
      - in: body
        name: item
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            price:
              type: number
    responses:
      200:
        description: Item updated successfully
      404:
        description: Item not found
    """
    item = Item.query.filter_by(category_id=category_id, id=item_id).first_or_404()
    data = request.get_json()
    for field in ["name", "description", "price"]:
        if field in data:
            setattr(item, field, data[field])
    db.session.commit()
    return item_schema.dump(item), 200


@category_bp.route("/categories/<int:category_id>/items/<int:item_id>/", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_item(category_id, item_id):
    """
    Delete an item under a category
    ---
    tags:
      - Item
    security:
      - BearerAuth: []
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
      - name: item_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Item deleted successfully
      404:
        description: Item not found
    """
    item = Item.query.filter_by(category_id=category_id, id=item_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200
