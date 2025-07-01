from flask_restx import Api
from flask import Flask
from app.config import Config
from app.extensions import db, ma, jwt, migrate
from flasgger import Swagger
from app.routes.auth_routes import auth_bp
from app.routes.restaurant_routes import restaurant_bp
from app.routes.branch_routes import branch_bp
from app.routes.menu_routes import menu_bp
from app.routes.category_item_routes import category_bp
from app.routes.order_routes import order_bp
from app.routes.table_routes import table_bp
from app.routes.reservation_routes import reservation_bp
from app.routes.invoice_routes import invoice_bp
from app.routes.report_routes import report_bp
from flasgger import Swagger

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Restaurant Management API",
        "description": "API Documentation for all endpoints",
        "version": "1.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
        }
    },
    "definitions": {
        "Restaurant": {
            "type": "object",
            "required": ["name", "location", "contact_number"],
            "properties": {
                "name": {"type": "string", "example": "Maheshwari's Diner"},
                "location": {"type": "string", "example": "Delhi, India"},
                "contact_number": {"type": "string", "example": "+91-9999999999"},
                "description": {"type": "string", "example": "Casual family restaurant"}
            }
        },
        "Branch": {
            "type": "object",
            "required": ["address", "city", "restaurant_id"],
            "properties": {
                "address": {"type": "string", "example": "123 Street"},
                "city": {"type": "string", "example": "Delhi"},
                "restaurant_id": {"type": "integer", "example": 1}
            }
        },
        "Category": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "example": "Starters"}
            }
        },
        "Item": {
            "type": "object",
            "required": ["name", "price", "category_id"],
            "properties": {
                "name": {"type": "string", "example": "Paneer Tikka"},
                "description": {"type": "string", "example": "Grilled paneer cubes with spices"},
                "price": {"type": "number", "format": "float", "example": 250.0},
                "category_id": {"type": "integer", "example": 1}
            }
        },
        "Table": {
            "type": "object",
            "required": ["table_number", "seats", "branch_id"],
            "properties": {
                "table_number": {"type": "string", "example": "T1"},
                "seats": {"type": "integer", "example": 4},
                "branch_id": {"type": "integer", "example": 1}
            }
        },
        "Reservation": {
            "type": "object",
            "required": ["customer_name", "table_id", "reservation_time"],
            "properties": {
                "customer_name": {"type": "string", "example": "Shivam Maheshwari"},
                "table_id": {"type": "integer", "example": 1},
                "reservation_time": {"type": "string", "format": "date-time", "example": "2025-06-25T18:30:00Z"}
            }
        },
        "OrderItem": {
            "type": "object",
            "required": ["order_id", "item_id", "quantity"],
            "properties": {
                "order_id": {"type": "integer", "example": 1},
                "item_id": {"type": "integer", "example": 2},
                "quantity": {"type": "integer", "example": 3}
            }
        },
        "Order": {
            "type": "object",
            "required": ["table_id"],
            "properties": {
                "table_id": {"type": "integer", "example": 1},
                "status": {"type": "string", "example": "pending"},
                "total_amount": {"type": "number", "format": "float", "example": 750.0}
            }
        },
        "Invoice": {
            "type": "object",
            "required": ["order_id", "total_amount"],
            "properties": {
                "order_id": {"type": "integer", "example": 1},
                "total_amount": {"type": "number", "format": "float", "example": 750.0},
                "paid": {"type": "boolean", "example": True}
            }
        },
        "Staff": {
            "type": "object",
            "required": ["username", "email", "password", "role"],
            "properties": {
                "username": {"type": "string", "example": "shivam_admin"},
                "email": {"type": "string", "example": "shivam@gmail.com"},
                "password": {"type": "string", "example": "secret123"},
                "role": {"type": "string", "enum": ["admin", "staff", "customer"], "example": "admin"}
            }
        }
    },
    "security": [{"BearerAuth": []}]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/swagger.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidoc",
    "swagger_ui_config": {
        "docExpansion": "none",
        "defaultModelsExpandDepth": -1
    }
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    Swagger(app, template=swagger_template, config=swagger_config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(table_bp)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(report_bp)

    with app.app_context():
        db.create_all()
    api = Api(app, doc='/apidoc', title="Restaurant Management API", description="API documentation")
    # api = Api(app)

    return app
