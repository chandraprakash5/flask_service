import declayer

import json
import logging
import os

from configobj import ConfigObj
from flask import Flask, Response, request, abort
from postgres_db_handler import PostgresDBHandler
from reviews_service import ReviewsServicer

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
config['db']['init_opts'] = "reflect_metadata"
db_handler = PostgresDBHandler(config['db'])

app = Flask(__name__)
reviews_servicer = ReviewsServicer(db_handler=db_handler)
app.logger.setLevel(logging.INFO)


@app.route('/healthz', methods=["GET"])
def healthz():
    return "OK"


@app.route('/reviews', methods=['GET'])
def list_reviews():
    app.logger.info("Log from reviews/reviews")
    model_number = request.args.get('model_number')
    if model_number is None:
        app.logger.error("Parameter model_number is missing")
        abort(400, "Parameter model_number is missing")
    limit = request.args.get('limit')
    if limit is None:
        limit = 20
    else:
        limit = int(limit)
    response_data = reviews_servicer.get_reviews(model_number=model_number, limit=limit)
    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/review', methods=['GET', 'POST'])
def review():
    app.logger.info("Log from reviews/review")
    response = None
    if request.method == 'GET':
        review_id = int(request.args.get('id'))
        if review_id is None:
            app.logger.error("Parameter review_id is missing")
            abort(400, "Parameter review_id is missing")
        try:
            review = reviews_servicer.get_review(review_id=review_id)
            response = app.response_class(
                response=json.dumps(review),
                status=200,
                mimetype='application/json'
            )
        except ValueError as e:
            app.logger.error("Error fetching review: %s" % e)
            abort(400, str(e))
        except Exception as e:
            app.logger.error("Internal error: %s" % e)
            abort(500)
    else:
        try:
            review_json = request.get_json()
            review_id = reviews_servicer.save_review(review_json=review_json)
            response = app.response_class(
                response=json.dumps(dict(review_id=review_id)),
                status=200,
                mimetype='application/json'
            )
        except ValueError as e:
            app.logger.error("Error fetching review: %s" % e)
            abort(400, str(e))
        except Exception as e:
            app.logger.error("Internal error: %s" % e)
            abort(500)
    return response


@app.route('/rating', methods=['GET'])
def product_ratings():
    app.logger.info("Log from reviews/avg_rating")
    model_number = request.args.get('model_number')
    if model_number is None:
        app.logger.error("Parameter model_number is missing")
        abort(400, "Parameter model_number is missing")
    avg_rating = reviews_servicer.get_avg_rating(model_number=model_number)
    response_data = dict(rating=avg_rating)
    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app_server_port = int(os.environ['APP_SERVER_PORT']) if 'APP_SERVER_PORT' in os.environ else 5000
    app.run(host='0.0.0.0', port=app_server_port)
