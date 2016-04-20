from flask import Flask, json, request, Response, jsonify
from DbConnection import db_session
from Models.CoffeeShop import CoffeeShop, CoffeeShopSchema
from Models.models import UserSchema, User
from werkzeug.exceptions import default_exceptions, HTTPException

schema = UserSchema()

__all__ = ['make_json_app']

def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.
    All error responses that you don't specifically
    manage yourself will have applications/json content
    type, and will contain JSON like this (just an example)
    {"message":"405: Method Not Allowed"}
    More here: http://flask.pocoo.org/snippets/83/
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex), code=(ex.code if isinstance(ex, HTTPException) else 500))
        response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
        return response
    app = Flask(import_name, **kwargs)
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error
    return app

app = make_json_app(__name__)

##Method based dispaching

@app.route('/coffeeShop', methods=['POST'])
def create_coffee_shop():
    #Takes as input a json message, parse it into CoffeeShop object and then insert it into database
    data = request.get_json()
    cs, errors = CoffeeShopSchema().load(data)
    if errors:
        return jsonify(errors)
    else:
        db_session.add(cs)
        db_session.commit()
        return cs


@app.route('/coffeeShops', methods=['GET'])
def get_coffee_shops():
    shops = CoffeeShop.query.all()
    cs, errors = CoffeeShopSchema(many=True).dumps(shops)
    # if errors:
        #ToDo return error
    return cs


@app.route('/coffeeShop/details', methods=['GET'])
def get_coffee_shop():
    id_req = request.args.get('id')
    id_req = hex(int(id_req))
    shops = CoffeeShop.query.filter(CoffeeShop.id_coffee_shop == id_req).filter()
    print(shops[0].id_coffee_shop)
    cs, errors = CoffeeShopSchema(many=True).dumps(shops)
    return cs


@app.route("/newUser", methods=['POST'])
def create_user():
    u, errors = UserSchema().load(request.args)
    if (errors):
        return Response(json.dumps(errors), mimetype='application/json', status=400)

    db_session.add(u)
    db_session.commit()

    return Response(UserSchema().dumps(u).data, mimetype='application/json')


@app.route('/users', methods=['GET'])
def get_users():
    service = request.args.get('service')

    users = User.query.filter(User.json.has_key(service)).all()

    users_serialized = schema.dumps(users, many=True).data
    return Response(users_serialized, mimetype='application/json')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
