from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS

mongo = PyMongo()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object("config.Config")

    # Initialize extensions
    CORS(app)
    mongo.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.matches import matches_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(matches_bp, url_prefix="/matches")

    # Health check
    @app.route("/health")
    def health():
        return {"status": "ok", "app": "orbit"}

    return app
