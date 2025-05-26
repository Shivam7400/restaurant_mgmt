from flask import Flask
from app.config import Config
from app.extensions import db, ma, jwt
from flask_migrate import Migrate
from app.routes.auth_routes import auth_bp
from app.routes.restaurant_routes import restaurant_bp
from app.routes.branch_routes import branch_bp
from app.routes.menu_routes import menu_bp
from app.extensions import db, ma, jwt, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(menu_bp)

    with app.app_context():
        db.create_all()

    return app
