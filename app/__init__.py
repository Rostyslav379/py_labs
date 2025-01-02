from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import ValidationError

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres_password@flask_app_db:5432/flask_app"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import User, Category, Record, Currency
    from app.routes import register_routes
    register_routes(app)

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    return app
