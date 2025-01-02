from datetime import datetime
from . import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    default_currency_id = db.Column(db.String(36), db.ForeignKey('currencies.id'), nullable=True)

    default_currency = relationship('Currency', back_populates='users')
    records = relationship('Record', back_populates='user')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    records = relationship('Record', back_populates='category')

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount_sum = db.Column(db.Float, nullable=False)

    user = relationship('User', back_populates='records')
    category = relationship('Category', back_populates='records')

class Currency(db.Model):
    __tablename__ = 'currencies'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = relationship('User', back_populates='default_currency')
