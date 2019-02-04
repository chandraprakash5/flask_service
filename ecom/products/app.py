import declayer

import json
import logging
import os

from configobj import ConfigObj
from flask import Flask, Response, request, abort
from postgres_db_handler import PostgresDBHandler
from products_service import ProductsServicer

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
products_servicer = ProductsServicer(reviews_addr=os.environ["REVIEWS_ADDR"],
                                     inventory_addr=os.environ["INVENTORY_ADDR"],
                                     db_handler=db_handler)
app.logger.setLevel(logging.INFO)


@app.route('/healthz', methods=["GET"])
def healthz():
    return "OK"


@app.route('/products', methods=['GET'])
def list_products():
    app.logger.info("Log from products/products")
    limit = request.args.get('limit')
    if limit is None:
        limit = 10
    else:
        limit = int(limit)
    response_data = list()
    for product in products_servicer.list_products(limit=limit):
        response_data.append(product)
    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/product', methods=['GET'])
def product():
    app.logger.info("Log from products/product")
    response = None
    product_id = int(request.args.get('id'))
    app.logger.info("Product id: %d" % product_id)
    try:
        product_dict = products_servicer.get_product(product_id=product_id)
        response = app.response_class(
            response=json.dumps(product_dict),
            status=200,
            mimetype='application/json'
        )
    except ValueError as e:
        app.logger.error("Error fetching product: %s" % e)
        abort(400, str(e))
    except Exception as e:
        app.logger.error("Internal error: %s" % e)
        abort(500)
    return response


if __name__ == '__main__':
    app_server_port = int(os.environ['APP_SERVER_PORT']) if 'APP_SERVER_PORT' in os.environ else 5000
    app.run(host='0.0.0.0', port=app_server_port)
