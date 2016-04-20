import uuid

import marshmallow.validate
from marshmallow import Schema, fields, post_load
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID, JSONB

from DbConnection import Base
from HelpFunctions.JsonField import Jsonlist


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    json = Column(JSONB)

    def __init__(self, name=None, email=None, json=None):
        self.name = name
        self.email = email
        self.json = json

    def __repr__(self):
        return '<User %r>' % (self.name)

class UserSchema(Schema):
    '''
    class Meta:
      fields = ("id", "name", "email", "uuid")
    '''
    id = fields.Integer()
    name = fields.Str(required=True, validate=marshmallow.validate.Length(min=1, max=2))
    email = fields.Email()
    uuid = fields.UUID()
    json = Jsonlist(required=True, validate=marshmallow.validate.Length(min=1))
    
    @post_load
    def createUser(self, data):
      return User(**data)
