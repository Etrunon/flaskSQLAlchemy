import json

from flask import Flask, request, Response, jsonify
from werkzeug.exceptions import default_exceptions, HTTPException

from DbConnection import db_session, get_base
from HelpFunctions.JsonException import InvalidUsage
from Models.CoffeeShop import CoffeeShop, CoffeeShopSchema

schema = CoffeeShopSchema()

__all__ = ['make_json_app']


class JsonRespose(Response):
    default_mimetype = 'application/json'


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

    for code, value in default_exceptions.items():
        app.error_handler_spec[None][code] = make_json_error
    return app


app = make_json_app(__name__)
app.response_class = JsonRespose
Base = get_base()


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# Method based dispaching

@app.route('/coffeeShop', methods=['POST'])
def create_coffee_shop():
    # Takes as input a json message, parse it into CoffeeShop object and then insert it into database
    data = request.get_json()
    cs, errors = CoffeeShopSchema().load(data)
    if errors:
        raise InvalidUsage(payload=errors)
    else:
        db_session.add(cs)
        db_session.commit()
        return CoffeeShopSchema().dumps(cs).data


@app.route('/coffeeShop', methods=['GET'])
def get_coffee_shop():
    id_req = request.args.get('id')

    # shops = db_session.query(CoffeeShop).filter(CoffeeShop.id_coffee_shop == id_req).all()
    shops = db_session.query(CoffeeShop).filter(CoffeeShop.id_coffee_shop == id_req).all()

    # shops[0].GeoPosition = json.loads(db_session.scalar(shops[0].position.ST_AsGeoJSON()))
    # print(shops[0].geo_position)

    cs, errors = CoffeeShopSchema(many=True).dumps(shops)
    return cs


@app.route('/coffeeShop/position', methods=['GET'])
def get_coffee_shop_position():
    id_req = request.args.get('id')
    shops = CoffeeShop.query.filter(CoffeeShop.id_coffee_shop == id_req)
    cs, errors = CoffeeShopSchema(many=True).dumps(shops)
    return cs


@app.route('/coffeeShops', methods=['GET'])
def get_coffee_shops():
    shops = CoffeeShop.query.all()
    cs, errors = CoffeeShopSchema(many=True).dumps(shops)
    # if errors:
    # ToDo return error
    return cs

# ToDo completare funzioni http
# @app.route('/delicacy', methods=['GET'])
# def get_real_product():
#     id_req = request.args.get('id')
#     product = RealProduct.query.filter(RealProduct.id_coffee_shop == id_req).filter()
#     print(shops[0].id_coffee_shop)
#     cs, errors = CoffeeShopSchema(many=True).dumps(shops)
#     return cs


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
