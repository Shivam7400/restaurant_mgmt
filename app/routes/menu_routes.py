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
    menus = Menu.query.all()
    return jsonify(menus_schema.dump(menus)), 200

@menu_bp.route("/<int:menu_id>", methods=["GET"])
@jwt_required()
def get_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    return jsonify(menu_schema.dump(menu)), 200

@menu_bp.route("/<int:menu_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_menu(menu_id):
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
    menu = Menu.query.get_or_404(menu_id)
    db.session.delete(menu)
    db.session.commit()
    return jsonify({"msg": "Menu item deleted"}), 200
