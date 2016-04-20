from flask import Flask, jsonify, json, request, Response, abort
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import Schema, fields
import marshmallow.validate
import uuid
import json
from Models.models import User, UserSchema
from db_connection import Base, db_session
from sqlalchemy.dialects.postgresql import UUID, JSONB

schema = UserSchema()

app = Flask(__name__)


@app.route("/newUser")
def createUser():
    u, errors = UserSchema().load(request.args);
    if (errors):
      return Response(json.dumps(errors), mimetype='application/json', status=400)
    
    db_session.add(u)
    db_session.commit()
    
    return Response(UserSchema().dumps(u).data, mimetype='application/json')


@app.route('/users')
def users():
    service = request.args.get('service')

    users = User.query.filter(User.json.has_key(service)).all()

    users_serialized = schema.dumps(users, many=True).data
    return Response(users_serialized, mimetype='application/json')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
