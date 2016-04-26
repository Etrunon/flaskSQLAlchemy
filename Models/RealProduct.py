from DbConnection import Base, add_query
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM, UUID, JSONB, REAL, BOOLEAN
from uuid import uuid4
from marshmallow import Schema, fields, post_load, validates
from HelpFunctions.CustomFields import Jsonlist
import marshmallow.validate

from HelpFunctions.Validate import validate_currency, validate_service

add_query(Base)


class RealProduct(Base):
    __tablename__ = 'real_products'
    id_real_product = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    id_coffee_shop = Column(UUID(as_uuid=True), ForeignKey('coffee_shops.id_coffee_shop'))
    name = Column(Text, unique=False, nullable=False)
    description = Column(Text, unique=False)
    image = Column(Text, unique=False)
    price = Column(REAL, unique=False)
    currency = Column(ENUM('eur', 'gpb', name='currency'), unique=False, nullable=False)
    enabled = Column(BOOLEAN, unique=False)
    services = Column(JSONB)

    def __init__(self, **kwargs):
        self.id_coffee_shop = kwargs.get('name')
        self.name = kwargs.get('email')
        self.description = kwargs.get('description')
        self.image = kwargs.get('currency')
        self.price = kwargs.get('currency')
        self.currency = kwargs.get('currency')
        self.enabled = kwargs.get('currency')
        self.services = kwargs.get('services')

    def __repr__(self):
        return '<User %r>' % (self.name)

    def __str__(self):
        return str(self.id_coffee_shop) + ' ' + self.name


class RealProductSchema(Schema):

    id_real_product = fields.Str()
    id_coffee_shop = fields.Str()
    name = fields.Str(required=True, validate=marshmallow.validate.Length(min=1, max=50))
    description = fields.Str()
    image = fields.Str()
    price = fields.Float(validate=marshmallow.validate.Range(min=0))
    currency = fields.Str()
    enabled = fields.Bool()
    services = Jsonlist()

    @post_load
    def create_real_product(self, data):
        return RealProduct(**data)

    @validates('currency')
    def validate_currency(self, data):
        return validate_currency(data)

    @validates('services')
    def validate_service(self, data):
        return validate_service(data)