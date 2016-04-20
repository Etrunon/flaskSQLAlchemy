from DbConnection import Base, addQuery
from sqlalchemy import Column, String, Text, REAL
from sqlalchemy.dialects.postgresql import ENUM, UUID
from uuid import uuid4

addQuery(Base)

class CoffeeShop(Base):
    __tablename__ = 'coffee_shops'
    id_coffee_shop = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=False, nullable=False)
    name = Column(String(50), unique=False, nullable=False)
    description = Column(Text, unique=False)
    address = Column(Text, unique=False)
    phone = Column(String(50), unique=False)
    currency = Column(ENUM('eur', 'gpb', name='currency'), unique=False, nullable=False)
    swift = Column(String(20), unique=False, nullable=False)
    iban = Column(String(20), unique=False, nullable=False)
    transaction_account = Column(Text, unique=True, nullable=False)
    latitude = Column(REAL, unique=False)
    longitude = Column(REAL, unique=False)

    # ToDo update time and creation time, services

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.currency = kwargs.get('currency')
        self.swift = kwargs.get('swift')
        self.iban = kwargs.get('iban')
        self.transaction_account = kwargs.get('transaction_account')

    def __repr__(self):
        return '<User %r>' % (self.name)

    def __str__(self):
        return str(self.id_coffee_shop) + ' ' + self.name
