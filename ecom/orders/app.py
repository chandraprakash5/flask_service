import declayer

import json
import logging
import os

from configobj import ConfigObj
from flask import Flask, Response, request, abort
from postgres_db_handler import PostgresDBHandler
from orders_service import OrdersServicer

config = ConfigObj(os.path.join(os.getcwd(), 'db_config'))
config = {
    'db': {
        'host': os.environ.get('DB_HOST','13.233.82.112'),
        'port': int(os.environ.get('DB_PORT', 5432)),
        'user': os.environ.get('DB_USER','ecom_user'),
        'password': os.environ.get('DB_PASSWORD', 'test_password'),
        'database': os.environ.get('DB_NAME','ecom'),
        'init_opts': 'reflect_metadata'
    }
}
db_handler = PostgresDBHandler(config['db'])

app = Flask(__name__)
orders_servicer = OrdersServicer(cart_addr=os.environ["CART_ADDR"], payments_addr=os.environ["PAYMENTS_ADDR"],
                                 inventory_addr=os.environ["INVENTORY_ADDR"], db_handler=db_handler)
app.logger.setLevel(logging.INFO)


@app.route('/healthz', methods=["GET"])
def healthz():
    return "OK"


@app.route('/user_orders', methods=['GET'])
def fetch_orders_for_user():
    app.logger.info("Log from orders/user_orders")
    user_id = request.args.get('user_id')
    if user_id is None:
        app.logger.error("Parameter user_id is missing")
        abort(400, "Parameter user_id is missing")
    else:
        user_id = int(user_id)
    limit = request.args.get('limit')
    if limit is None:
        limit = 10
    else:
        limit = int(limit)
    orders = orders_servicer.list_orders_for_user(user_id=user_id, limit=limit)
    response = app.response_class(
        response=json.dumps(orders),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/order', methods=['GET', 'POST'])
def order():
    app.logger.info("Log from orders/order")
    response = None
    if request.method == 'GET':
        order_id = request.args.get('id')
        if order_id is None:
            app.logger.error("Parameter id is missing")
            abort(400, "Parameter id is missing")
        else:
            order_id = int(order_id)
        app.logger.info("Fetching order details for id: %d", order_id)
        try:
            order_dict = orders_servicer.get_order_details(order_id=order_id)
            response = app.response_class(
                response=json.dumps(order_dict),
                status=200,
                mimetype='application/json'
            )
        except ValueError as e:
            app.logger.error("Error fetching order: %s" % e)
            abort(400, str(e))
        except Exception as e:
            app.logger.error("Internal error: %s" % e)
            abort(500)
    else:
        user_id = int(request.args.get('user_id'))
        order_json = request.get_json()
        app.logger.info("Creating order for user id: %d" % user_id)
        try:
            order_dict = orders_servicer.create_order(user_id=user_id, delivery_address=order_json["delivery_address"])
            response = app.response_class(
                response=json.dumps(order_dict),
                status=200,
                mimetype='application/json'
            )
        except ValueError as e:
            app.logger.error("Error creating order: %s" % e)
            abort(400, str(e))
        except Exception as e:
            app.logger.error("Internal error: %s" % e)
            abort(500)
    return response


@app.route('/update_payment_status', methods=['PUT'])
def update_payment_status():
    app.logger.info("Log from orders/order")
    response = None
    order_id = request.args.get('id')
    if order_id is None:
        app.logger.error("Parameter id is missing")
        abort(400, "Parameter id is missing")
    else:
        order_id = int(order_id)
    payment_status = request.args.get('status')
    if payment_status is None:
        app.logger.error("Parameter status is missing")
        abort(400, "Parameter status is missing")
    try:
        ack = orders_servicer.update_payment_status(order_id=order_id, payment_status=payment_status)
        response = app.response_class(
            response=json.dumps(ack),
            status=200,
            mimetype='application/json'
        )
    except ValueError as e:
        app.logger.error("Error creating order: %s" % e)
        abort(400, str(e))
    except Exception as e:
        app.logger.error("Internal error: %s" % e)
        abort(500)
    return response


if __name__ == '__main__':
    app_server_port = int(os.environ['APP_SERVER_PORT']) if 'APP_SERVER_PORT' in os.environ else 5000
    app.run(host='0.0.0.0', port=app_server_port)
