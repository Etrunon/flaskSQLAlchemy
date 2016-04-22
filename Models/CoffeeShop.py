from uuid import uuid4

import marshmallow.validate
from marshmallow import Schema, fields, post_load, validates
from sqlalchemy import Column, String, Text, REAL
from sqlalchemy.dialects.postgresql import ENUM, UUID, JSONB

from DbConnection import Base, add_query
from HelpFunctions.JsonField import Jsonlist
from HelpFunctions.Validate import validate_currency, validate_service

add_query(Base)


class CoffeeShop(Base):
    __tablename__ = 'coffee_shops'
    id_coffee_shop = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    username = Column(Text, unique=True, nullable=False)
    password = Column(Text, unique=False, nullable=False)
    name = Column(Text, unique=False, nullable=False)
    image = Column(Text, unique=False)
    description = Column(Text, unique=False)
    address = Column(Text, unique=False)
    phone = Column(Text, unique=False)
    currency = Column(ENUM('eur', 'gpb', name='currency'), unique=False, nullable=False)
    swift = Column(Text, unique=False, nullable=False)
    iban = Column(Text, unique=False, nullable=False)
    transaction_account = Column(Text, unique=True, nullable=False)
    latitude = Column(REAL, unique=False)
    longitude = Column(REAL, unique=False)
    services = Column(JSONB)

    # ToDo update time and creation time, services

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.currency = kwargs.get('currency')
        self.swift = kwargs.get('swift')
        self.iban = kwargs.get('iban')
        self.description = kwargs.get('description')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.address = kwargs.get('address')
        self.phone = kwargs.get('phone')
        self.transaction_account = kwargs.get('transaction_account')
        self.services = kwargs.get('services')

    def __repr__(self):
        return '<User %r>' % (self.name)

    def __str__(self):
        return str(self.id_coffee_shop) + ' ' + self.name


class CoffeeShopSchema(Schema):

    id_coffee_shop = fields.Str()
    username = fields.Str(required=True, validate=marshmallow.validate.Length(min=4, max=50))
    password = fields.Str(required=True, validate=marshmallow.validate.Length(min=6, max=50))
    name = fields.Str(required=True, validate=marshmallow.validate.Length(min=1, max=50))
    description = fields.Str()
    address = fields.Str()
    phone = fields.Str(validate=marshmallow.validate.Length(max=50))
    currency = fields.Str()
    swift = fields.Str(validate=marshmallow.validate.Length(max=20))
    iban = fields.Str(validate=marshmallow.validate.Length(max=20))
    transaction_account = fields.Str()
    latitude = fields.Float(validate=marshmallow.validate.Range(min=-90, max=90))
    longitude = fields.Float(validate=marshmallow.validate.Range(min=-180, max=180))
    services = Jsonlist(validate=marshmallow.validate.Length(min=1))

    @post_load
    def create_user(self, data):
        return CoffeeShop(**data)

    @validates('currency')
    def validate_currency(self, data):
        return validate_currency(self, data)

    @validates('service')
    def validate_service(self, data):
        return validate_service(self, data)