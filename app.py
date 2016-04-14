from flask import Flask, jsonify, json, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    'postgresql://postgres:@postgres/', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

    def __str__(self):
        return str(self.id) + ' ' + self.name + ' ' + self.email


app = Flask(__name__)


@app.route("/newUser")
def createUser():
    u = User(request.args.get('name'), request.args.get('email'))
    db_session.add(u)
    db_session.commit()
    return "Created user " + u.name + " with id " + str(u.id)


@app.route('/users')
def users():
    users = User.query.all()
    return json.dumps([str(ob) for ob in users])


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
