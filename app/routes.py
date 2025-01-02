from flask import Blueprint, request, jsonify
from uuid import uuid4
from .models import User, Category, Record, Currency
from .schemas import UserSchema, CategorySchema, RecordSchema, CurrencySchema
from . import db

api = Blueprint('api', __name__)

# User routes
@api.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    schema = UserSchema()
    user_data = schema.load(data)

    default_currency = user_data.get("default_currency_id")
    if default_currency:
        currency = Currency.query.filter_by(name=default_currency).first()
        if not currency:
            return jsonify({"error": "Currency not found"}), 400
        user_data["default_currency_id"] = currency.id
    else:
        currency = Currency.query.filter_by(name="USD").first()
        user_data["default_currency_id"] = currency.id

    user = User(id=uuid4().hex, **user_data)
    db.session.add(user)
    db.session.commit()
    return schema.dump(user), 201

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    schema = UserSchema(many=True)
    return schema.dump(users)

# Category routes
@api.route("/category", methods=["POST"])
def create_category():
    data = request.get_json()
    schema = CategorySchema()
    category_data = schema.load(data)
    category = Category(id=uuid4().hex, **category_data)
    db.session.add(category)
    db.session.commit()
    return schema.dump(category), 201

@api.route("/category", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    schema = CategorySchema(many=True)
    return schema.dump(categories)

# Record routes
@api.route("/record", methods=["POST"])
def create_record():
    data = request.get_json()
    schema = RecordSchema()
    record_data = schema.load(data)
    record = Record(id=uuid4().hex, **record_data)
    db.session.add(record)
    db.session.commit()
    return schema.dump(record), 201

@api.route("/record", methods=["GET"])
def get_records():
    records = Record.query.all()
    schema = RecordSchema(many=True)
    return schema.dump(records)

@api.route("/healthcheck", methods=["GET"])
def healthcheck():
    return "OK"
def register_routes(app):
    app.register_blueprint(api)
