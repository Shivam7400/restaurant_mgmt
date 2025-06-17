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

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    Swagger(app)

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

    return app
