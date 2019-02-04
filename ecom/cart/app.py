import declayer

import json
import logging
import os

from flask import Flask, Response, request, abort
from cart_service import CartServicer

app = Flask(__name__)
cart_servicer = CartServicer(redis_host=os.environ["REDIS_HOST"], redis_port=os.environ["REDIS_PORT"])
app.logger.setLevel(logging.INFO)


@app.route('/healthz', methods=["GET"])
def healthz():
    return "OK"


@app.route('/add_item', methods=['PUT'])
def add_item():
    app.logger.info("Log from cart/add_item")

    user_id = request.args.get('user_id')
    if user_id is None:
        app.logger.error("Parameter user_id is missing")
        abort(400, "Parameter user_id is missing")
    user_id = int(user_id)

    listing_id = request.args.get('listing_id')
    if listing_id is None:
        app.logger.error("Parameter listing_id is missing")
        abort(400, "Parameter listing_id is missing")
    listing_id = int(listing_id)

    response_data = cart_servicer.add_item_to_cart(user_id=user_id, listing_id=listing_id)
    response = app.response_class(
        response=response_data,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/remove_item', methods=['PUT'])
def remove_item():
    app.logger.info("Log from cart/remove_item")

    user_id = request.args.get('user_id')
    if user_id is None:
        app.logger.error("Parameter user_id is missing")
        abort(400, "Parameter user_id is missing")
    user_id = int(user_id)

    listing_id = request.args.get('listing_id')
    if listing_id is None:
        app.logger.error("Parameter listing_id is missing")
        abort(400, "Parameter listing_id is missing")
    listing_id = int(listing_id)

    try:
        response_data = cart_servicer.remove_item_to_cart(user_id=user_id, listing_id=listing_id)
        response = app.response_class(
            response=response_data,
            status=200,
            mimetype='application/json'
        )
        return response
    except ValueError as e:
        app.logger.error("Error updating cart: %s" % e)
        abort(400, str(e))
    except Exception as e:
        app.logger.error("Internal error: %s" % e)
        abort(500)


@app.route('/items', methods=['GET', 'DELETE'])
def list_items():
    app.logger.info("Log from cart/items")

    user_id = request.args.get('user_id')
    if user_id is None:
        app.logger.error("Parameter user_id is missing")
        abort(400, "Parameter user_id is missing")
    user_id = int(user_id)

    if request.method == 'GET':
        response_data = cart_servicer.list_items_in_cart(user_id=user_id)
        response = app.response_class(
            response=response_data,
            status=200,
            mimetype='application/json'
        )
        return response

    response_data = cart_servicer.clear_cart(user_id=user_id)
    response = app.response_class(
        response=response_data,
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app_server_port = int(os.environ['APP_SERVER_PORT']) if 'APP_SERVER_PORT' in os.environ else 5000
    app.run(host='0.0.0.0', port=app_server_port)
