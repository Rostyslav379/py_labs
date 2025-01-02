from marshmallow import Schema, fields, validates, ValidationError

from app.models import Currency


class CurrencySchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    default_currency_id = fields.Str()

    @validates("default_currency_id")
    def validate_currency(self, value):
        currency = Currency.query.filter_by(name=value).first()
        if not currency:
            raise ValidationError("Invalid currency name.")

class CategorySchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

    @validates("name")
    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError("Category name must be at least 2 characters long.")

class RecordSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    category_id = fields.Str(required=True)
    created_date = fields.DateTime(dump_only=True)
    amount_sum = fields.Float(required=True)

    @validates("amount_sum")
    def validate_amount_sum(self, value):
        if value <= 0:
            raise ValidationError("Amount must be greater than zero.")
