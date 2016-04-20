from flask import Flask, json, request
from DbConnection import db_session, Base

from Models.CoffeeShop import CoffeeShop

app = Flask(__name__)

##Method based dispaching


# @app.route("/newUser")
# def createUser():
#     # u = User(request.args.get('name'), request.args.get('email'))
#     db_session.add(u)
#     db_session.commit()
#     return "Created user " + u.name + " with id " + str(u.id)

# app.add_url_rule("/getShop", view_func=getShop)

@app.route('/test')
def test():
    c = CoffeeShop(name='Pippo', email='google', currency='eur', iban='12', swift='13', username='ciao', password='pass', transaction_account='trans')
    print(c.id_coffee_shop)
    db_session.add(c)
    db_session.commit()

@app.route('/coffeeShops')
def users():
    users = CoffeeShop.query.all()
    return json.dumps([str(ob) for ob in users])


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

