from flask import Blueprint, request, jsonify
from app.models.menu import Menu
from app.extensions import db
from app.schemas.menu_schema import MenuSchema
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required

menu_bp = Blueprint("menu", __name__, url_prefix="/menus")
menu_schema = MenuSchema()
menus_schema = MenuSchema(many=True)

@menu_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_menu():
    """
    Create a new menu item
    ---
    tags:
      - Menu
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              price:
                type: number
              category:
                type: string
              restaurant_id:
                type: integer
            required:
              - name
              - price
              - category
              - restaurant_id
    responses:
      201:
        description: Menu item created
      400:
        description: Validation error
    """
    data = request.get_json()
    errors = menu_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    menu = Menu(**data)
    db.session.add(menu)
    db.session.commit()
    # return menu_schema.jsonify(menu), 201
    return jsonify(menu_schema.dump(menu)), 201

@menu_bp.route("/", methods=["GET"])
@jwt_required()
def get_menus():
    """
    Get all menu items
    ---
    tags:
      - Menu
    security:
      - BearerAuth: []
    responses:
      200:
        description: A list of all menu items
    """
    menus = Menu.query.all()
    return jsonify(menus_schema.dump(menus)), 200

@menu_bp.route("/<int:menu_id>", methods=["GET"])
@jwt_required()
def get_menu(menu_id):
    """
    Get a specific menu item by ID
    ---
    tags:
      - Menu
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: menu_id
        required: true
        schema:
          type: integer
        description: The ID of the menu item
    responses:
      200:
        description: Menu item data
      404:
        description: Menu item not found
    """
    menu = Menu.query.get_or_404(menu_id)
    return jsonify(menu_schema.dump(menu)), 200

@menu_bp.route("/<int:menu_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_menu(menu_id):
    """
    Update a menu item
    ---
    tags:
      - Menu
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: menu_id
        required: true
        schema:
          type: integer
        description: ID of the menu item
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              price:
                type: number
              category:
                type: string
              restaurant_id:
                type: integer
    responses:
      200:
        description: Menu item updated
      404:
        description: Menu item not found
    """
    menu = Menu.query.get_or_404(menu_id)
    data = request.get_json()
    for field in ["name", "price", "category", "restaurant_id"]:
        if field in data:
            setattr(menu, field, data[field])
    db.session.commit()
    return jsonify(menu_schema.dump(menu)), 200

@menu_bp.route("/<int:menu_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_menu(menu_id):
    """
    Delete a menu item
    ---
    tags:
      - Menu
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: menu_id
        required: true
        schema:
          type: integer
        description: ID of the menu item to delete
    responses:
      200:
        description: Menu item deleted successfully
      404:
        description: Menu item not found
    """
    menu = Menu.query.get_or_404(menu_id)
    db.session.delete(menu)
    db.session.commit()
    return jsonify({"msg": "Menu item deleted"}), 200
