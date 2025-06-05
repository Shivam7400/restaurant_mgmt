from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.table import Table
from app.schemas.table_schema import TableSchema
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required

table_bp = Blueprint("tables", __name__, url_prefix="/tables")

table_schema = TableSchema()
tables_schema = TableSchema(many=True)

@table_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_table():
    data = request.get_json()
    table = table_schema.load(data)
    db.session.add(table)
    db.session.commit()
    return table_schema.jsonify(table), 201

@table_bp.route("/", methods=["GET"])
@jwt_required()
def get_tables():
    tables = Table.query.all()
    return tables_schema.jsonify(tables), 200

@table_bp.route("/<int:table_id>", methods=["GET"])
@jwt_required()
def get_table(table_id):
    table = Table.query.get_or_404(table_id)
    return table_schema.jsonify(table), 200

@table_bp.route("/<int:table_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_table(table_id):
    table = Table.query.get_or_404(table_id)
    data = request.get_json()
    updated_table = table_schema.load(data, instance=table, partial=True)
    db.session.commit()
    return table_schema.jsonify(updated_table), 200

@table_bp.route("/<int:table_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_table(table_id):
    table = Table.query.get_or_404(table_id)
    db.session.delete(table)
    db.session.commit()
    return jsonify({"message": "Table deleted successfully"}), 200
