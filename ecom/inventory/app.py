import declayer

import json
import logging
import os

from configobj import ConfigObj
from flask import Flask, Response, request, abort
from postgres_db_handler import PostgresDBHandler
from inventory_service import InventoryServicer

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
inventory_servicer = InventoryServicer(db_handler=db_handler)
app.logger.setLevel(logging.INFO)


@app.route('/healthz', methods=["GET"])
def healthz():
    return "OK"


@app.route('/fetch_availability', methods=['GET'])
def get_availability():
    app.logger.info("Log from inventory/fetch_availability")
    listing_ids = request.args.get('listing_ids')
    if listing_ids is None:
        app.logger.error("Parameter order_id is missing")
        abort(400, "Parameter order_id is missing")
    else:
        listing_ids = listing_ids.split(',')
        listing_ids = [int(listing_id.strip()) for listing_id in listing_ids]
    response = None
    try:
        availability_dict = inventory_servicer.get_availability(listing_ids=listing_ids)
        response = app.response_class(
            response=json.dumps(availability_dict),
            status=200,
            mimetype='application/json'
        )
    except ValueError as e:
        app.logger.error("Error fetching availability: %s" % e)
        abort(400, str(e))
    except Exception as e:
        app.logger.error("Internal error: %s" % e)
        abort(500)
    return response


@app.route('/fetch_details', methods=['GET'])
def get_details():
    app.logger.info("Log from inventory/fetch_details")
    listing_ids = request.args.get('listing_ids')
    if listing_ids is None:
        app.logger.error("Parameter order_id is missing")
        abort(400, "Parameter order_id is missing")
    else:
        listing_ids = listing_ids.split(',')
        listing_ids = [int(listing_id.strip()) for listing_id in listing_ids]
    estimate_delivery = request.args.get('estimate_delivery')
    if estimate_delivery is None:
        estimate_delivery = False
    else:
        estimate_delivery = bool(estimate_delivery)
    dest = request.args.get('dest')
    if estimate_delivery and not dest:
        app.logger.error("Parameter dest is mandatory if estimate_delivery is set to 1")
        abort(400, "Parameter dest is mandatory if estimate_delivery is set to 1")
    response = None
    try:
        listing_details = inventory_servicer.get_listing_details(listing_ids=listing_ids,
                                                                 estimate_delivery=estimate_delivery,
                                                                 dest_addr=dest)
        response = app.response_class(
            response=json.dumps(listing_details),
            status=200,
            mimetype='application/json'
        )
    except ValueError as e:
        app.logger.error("Error fetching listings' details: %s" % e)
        abort(400, str(e))
    except Exception as e:
        app.logger.error("Internal error: %s" % e)
        abort(500)
    return response


@app.route('/listings', methods=['GET'])
def fetch_listings():
    app.logger.info("Log from inventory/listings")
    response = None
    product_id = request.args.get('product_id')
    if product_id is None:
        app.logger.error("Parameter product_id is missing")
        abort(400, "Parameter product_id is missing")
    else:
        product_id = int(product_id)
    limit = request.args.get('limit')
    if limit is None:
        limit = 10
    else:
        limit = int(limit)
    app.logger.info("Product id: %d" % product_id)
    try:
        listings = inventory_servicer.get_listings_for_product(product_id=product_id, limit=limit)
        response = app.response_class(
            response=json.dumps(listings),
            status=200,
            mimetype='application/json'
        )
    except ValueError as e:
        app.logger.error("Error fetching listings: %s" % e)
        abort(400, str(e))
    except Exception as e:
        app.logger.error("Internal error: %s" % e)
        abort(500)
    return response


if __name__ == '__main__':
    app_server_port = int(os.environ['APP_SERVER_PORT']) if 'APP_SERVER_PORT' in os.environ else 5000
    app.run(host='0.0.0.0', port=app_server_port)
