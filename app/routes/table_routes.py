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
    """
    Create a new table
    ---
    tags:
      - Tables
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/definitions/Table'
    responses:
      201:
        description: Table created successfully
        schema:
          $ref: '#/definitions/Table'
      400:
        description: Validation failed
    """
    data = request.get_json()
    table = table_schema.load(data)
    db.session.add(table)
    db.session.commit()
    return table_schema.jsonify(table), 201

@table_bp.route("/", methods=["GET"])
@jwt_required()
def get_tables():
    """
    Get all tables
    ---
    tags:
      - Tables
    security:
      - BearerAuth: []
    responses:
      200:
        description: A list of all tables
        schema:
          type: array
          items:
            $ref: '#/definitions/Table'
    """
    tables = Table.query.all()
    return tables_schema.jsonify(tables), 200

@table_bp.route("/<int:table_id>", methods=["GET"])
@jwt_required()
def get_table(table_id):
    """
    Get a specific table by ID
    ---
    tags:
      - Tables
    security:
      - BearerAuth: []
    parameters:
      - name: table_id
        in: path
        type: integer
        required: true
        description: ID of the table
    responses:
      200:
        description: Table details
        schema:
          $ref: '#/definitions/Table'
      404:
        description: Table not found
    """
    table = Table.query.get_or_404(table_id)
    return table_schema.jsonify(table), 200

@table_bp.route("/<int:table_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_table(table_id):
    """
    Update a table by ID
    ---
    tags:
      - Tables
    security:
      - BearerAuth: []
    parameters:
      - name: table_id
        in: path
        type: integer
        required: true
        description: ID of the table to update
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/definitions/Table'
    responses:
      200:
        description: Table updated
        schema:
          $ref: '#/definitions/Table'
      404:
        description: Table not found
    """
    table = Table.query.get_or_404(table_id)
    data = request.get_json()
    updated_table = table_schema.load(data, instance=table, partial=True)
    db.session.commit()
    return table_schema.jsonify(updated_table), 200

@table_bp.route("/<int:table_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_table(table_id):
    """
    Delete a table by ID
    ---
    tags:
      - Tables
    security:
      - BearerAuth: []
    parameters:
      - name: table_id
        in: path
        type: integer
        required: true
        description: ID of the table to delete
    responses:
      200:
        description: Table deleted successfully
      404:
        description: Table not found
    """
    table = Table.query.get_or_404(table_id)
    db.session.delete(table)
    db.session.commit()
    return jsonify({"message": "Table deleted successfully"}), 200
