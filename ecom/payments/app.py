import declayer

import json
import logging
import os

from configobj import ConfigObj
from flask import Flask, Response, request, abort
from postgres_db_handler import PostgresDBHandler
from payments_service import PaymentsServicer

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
payments_servicer = PaymentsServicer(orders_addr=os.environ["ORDERS_ADDR"], db_handler=db_handler)
app.logger.setLevel(logging.INFO)


@app.route('/healthz', methods=["GET"])
def healthz():
    return "OK"


@app.route('/payment_details', methods=['GET'])
def get_payment_details():
    app.logger.info("Log from payments/payment_details")
    response = None
    order_id = request.args.get('order_id')
    if order_id is None:
        app.logger.error("Parameter order_id is missing")
        abort(400, "Parameter order_id is missing")
    else:
        order_id = int(order_id)
    try:
        payment_dict = payments_servicer.get_payment(order_id=order_id)
        response = app.response_class(
            response=json.dumps(payment_dict),
            status=200,
            mimetype='application/json'
        )
    except ValueError as e:
        app.logger.error("Error fetching payment for order: %s" % e)
        abort(400, str(e))
    except Exception as e:
        app.logger.error("Internal error: %s" % e)
        abort(500)
    return response


@app.route('/pay', methods=['POST'])
def pay():
    app.logger.info("Log from payments/pay")
    response = None
    order_id = request.args.get('order_id')
    if order_id is None:
        app.logger.error("Parameter order_id is missing")
        abort(400, "Parameter order_id is missing")
    else:
        order_id = int(order_id)
    payment_details = request.get_json()
    app.logger.debug("Order id: %d" % order_id)
    try:
        response = payments_servicer.initiate_payment(order_id=order_id, mode=payment_details["mode"],
                                                      mode_details=payment_details["mode_details"],
                                                      amount=payment_details["amount"])
        response = app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
    except ValueError as e:
        app.logger.error("Error initiating payment: %s" % e)
        abort(400, str(e))
    except Exception as e:
        app.logger.error("Internal error: %s" % e)
        abort(500)
    return response


@app.route('/payment_callback', methods=['PUT'])
def payment_callback():
    app.logger.info("Log from payments/payment_callback")
    response = None
    payment_id = request.args.get('id')
    if payment_id is None:
        app.logger.error("Parameter payment_id is missing")
        abort(400, "Parameter payment_id is missing")
    else:
        payment_id = int(payment_id)
    transaction_details = request.get_json()
    error_details = transaction_details["error_message"] if "error_message" in transaction_details else None
    try:
        payments_servicer.handle_payment_callback(payment_id=payment_id,
                                                  success=bool(int(transaction_details["success"])),
                                                  error_details=error_details)
        response = app.response_class(
            response="OK",
            status=200,
            mimetype='application/text'
        )
    except Exception as e:
        app.logger.error("Internal error: %s" % e)
        abort(500)
    return response


if __name__ == '__main__':
    app_server_port = int(os.environ['APP_SERVER_PORT']) if 'APP_SERVER_PORT' in os.environ else 5000
    app.run(host='0.0.0.0', port=app_server_port)
