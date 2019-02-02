import json
from flask import Flask, Response, request, jsonify

import logging
import os

import grpc

from flask import Flask, Response, request
from flask_opentracing import FlaskTracer
from jaeger_client import Config
from prometheus_client import Counter, Summary, Gauge, generate_latest

from external_libs import ProductId, Product, ProductsStub
import json
import time

from external_libs import ProductId, Limit, Product, ProductsStub, \
    ReviewsStub, SimilarProductsStub, UserId, Review, ReviewsRequest, \
    ReviewId, SimilarProductRequest, ReviewedProduct


REQUESTS = Counter('http_request_count', 'Total http requests requested.', labelnames=['http_status'])
REQUEST_TIME = Summary('http_request_processing_seconds', 'Time spent processing request')
IN_PROGRESS = Gauge('http_request_in_progress', 'Number of requests in progress')
REQUEST_SIZE = Summary('http_request_size_bytes', 'Size of requests',)
RESPONSE_SIZE = Summary('http_response_size_bytes', 'Size of response')
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


def create_tracer(service_name):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': os.environ['DECL_JAEGER_AGENT_HOST'],
                'reporting_port': os.environ['DECL_JAEGER_AGENT_COMPACT_PORT'],
            },
            'logging': True,
        },
        service_name=service_name,
    )
    tracer = config.initialize_tracer()
    return tracer


app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)
flask_tracer = FlaskTracer(create_tracer('flask'), True, app)

review_channel = grpc.insecure_channel('com-declayer-store-reviews:5000')
review_stub = ReviewsStub(channel=review_channel)

product_channel = grpc.insecure_channel('com-declayer-store-products:5000')
product_stub = ProductsStub(channel=product_channel)

similar_channel = grpc.insecure_channel('com-declayer-store-similarproducts:5000')
similar_stub = SimilarProductsStub(channel=similar_channel)


@REQUEST_TIME.time()
def process_request():
    # app.logger.info("Count received = %s", count)
    # id, name, desc, category_id, keywords, photoUrls
    product = Product(
        name='IFB Easy Cook',
        description='IFB Microwave',
        category_id='Home Electronics',
        keywords=['home appliances', 'microwave', 'convection']
    )

    product_id = product_stub.SaveProduct(product)
    app.logger.info("Product id = %s", product_id.id)
    return product_id.id


# @app.route('/', methods=['GET', 'POST'])
# def hello_world():
#     REQUESTS.labels(200).inc()
#     IN_PROGRESS.inc()
#     app.logger.info("Log from docker")
#     count = process_request()
#     response = 'Flask Dockerized = ' + str(count)
#     request_bytes = 0
#     if request.data:
#         request_bytes = len(request.data.encode('utf-8'))
#     REQUEST_SIZE.observe(request_bytes)
#     RESPONSE_SIZE.observe(len(response.encode('utf-8')))
#     IN_PROGRESS.dec()
#     return response


@REQUEST_TIME.time()
def save_product(product_info):
    # id, name, desc, category_id, keywords, photoUrls
    product = Product(
        name=product_info['name'],
        description=product_info['description'],
        category_id=product_info['category_id'],
        keywords=product_info['keywords']
    )
    product_id = product_stub.SaveProduct(product)
    app.logger.info("Product id = %s" % product_id.id)
    return product_id.id


def get_review_list(reviews):
    review_info = []
    for review in reviews:
        review_info.append(
            {
                'review_id': review.id.id,
                'product_id': review.productId.id,
                'review': review.reviewText,
                'timestamp': review.lastUpdatedTimestamp
            }
        )
    return review_info


def get_product_dict(product):
    product_dict = {}
    if product.name:
        product_dict = {
            'name': product.name,
            'description': product.description,
            'category_id': product.category_id,
            'keywords': product.keywords
        }
    return product_dict


@REQUEST_TIME.time()
def get_product(product_id):
    try:
        reviewed_product = product_stub.GetProduct(ProductId(id=product_id))
    except grpc.RpcError as e:
        return {'error': 'UNAVAILABLE'}
    product_info = {'product': get_product_dict(reviewed_product.product),
                    'reviews': get_review_list(reviewed_product.reviews)}
    return product_info


# We will send this:
# {
# 	"name": "IFB Easy Cook",
# 	"description": "IFB Microwave",
# 	"category_id": "Home Electronics",
# 	"keywords": ["home appliances", "microwave", "convection"]
# }
@app.route('/product', methods=['GET', 'POST'])
def product():
    REQUESTS.labels(200).inc()
    IN_PROGRESS.inc()
    app.logger.info("Log from flask/product")
    request_bytes = 0
    if request.method == 'GET':
        product_id = request.args.get('id')
        data = str(get_product(int(product_id)))
        response = app.response_class(
            response=json.dumps(eval(data)),
            status=200,
            mimetype='application/json'
        )
        RESPONSE_SIZE.observe(len(data.encode('utf-8')))
    else:
        if request.data:
            request_bytes = len(request.data)
            app.logger.info("Request bytes = %s" % request_bytes)
        product_info = json.loads(request.data)
        product_id = save_product(product_info)
        response = "Saved Product with id: %s" % product_id
        RESPONSE_SIZE.observe(len(response.encode('utf-8')))
    REQUEST_SIZE.observe(request_bytes)
    IN_PROGRESS.dec()
    return response



# We will send this:
# {
# 	"product_id": 1,
# 	"user_id": 1,
# 	"review": "This is the worst product. Avoid!!"
# }
@REQUEST_TIME.time()
def save_review(review_info):
    review = Review(
        productId=ProductId(id=review_info['product_id']),
        userId=UserId(id=review_info['user_id']),
        reviewTimestamp=int(time.time()),
        lastUpdatedTimestamp=int(time.time()),
        reviewText=review_info['review'])
    review_id = review_stub.SaveReview(review)
    app.logger.info("Review id = %s" % review_id.id)
    return review_id.id


@REQUEST_TIME.time()
def get_review(product_id, limit):
    reviews_products_req = ReviewsRequest(productId=ProductId(id=product_id), limit=Limit(limit=limit))
    try:
        reviews = review_stub.GetReviews(reviews_products_req)
    except grpc.RpcError as e:
        return {'error': 'UNAVAILABLE'}
    reviews = [r for r in reviews]
    return get_review_list(reviews)


@app.route('/review', methods=['GET', 'POST'])
def review():
    REQUESTS.labels(200).inc()
    IN_PROGRESS.inc()
    app.logger.info("Log from flask/review")
    request_bytes = 0
    if request.method == 'GET':
        product_id = request.args.get('id')
        limit = request.args.get('limit')
        data = str(get_review(int(product_id), int(limit)))
        response = app.response_class(
            response=json.dumps(eval(data)),
            status=200,
            mimetype='application/json'
        )
        RESPONSE_SIZE.observe(len(data.encode('utf-8')))
    else:
        if request.data:
            request_bytes = len(request.data)
            app.logger.info("Request bytes = %s" % request_bytes)
        review_info = json.loads(request.data)
        review_id = save_review(review_info)
        response = "Saved Review with id: %s" % review_id
        RESPONSE_SIZE.observe(len(response.encode('utf-8')))
    REQUEST_SIZE.observe(request_bytes)
    IN_PROGRESS.dec()
    return response


@REQUEST_TIME.time()
def get_similar(product_id, limit):
    similar_products_req = SimilarProductRequest(productId=ProductId(id=product_id), limit=Limit(limit=limit))
    similar_product = similar_stub.GetSimilarProducts(similar_products_req)
    similar_products = [p for p in similar_product]
    similar_product_info = []
    for reviewed_product in similar_products:
        if reviewed_product.product:
            similar_product_info.append(
                {
                    'product': get_product_dict(reviewed_product.product),
                    'reviews': get_review_list(reviewed_product.reviews)
                }
            )
    return similar_product_info


@app.route('/similar', methods=['GET'])
def similar():
    REQUESTS.labels(200).inc()
    IN_PROGRESS.inc()
    app.logger.info("Log from flask/similar")
    request_bytes = 0
    product_id = request.args.get('id')
    limit = request.args.get('limit')
    data = str(get_similar(int(product_id), int(limit)))
    response = app.response_class(
        response=json.dumps(eval(data)),
        status=200,
        mimetype='application/json'
    )
    REQUEST_SIZE.observe(request_bytes)
    RESPONSE_SIZE.observe(len(data.encode('utf-8')))
    IN_PROGRESS.dec()
    return response


@app.route('/all', methods=['GET'])
def all():
    REQUESTS.labels(200).inc()
    IN_PROGRESS.inc()
    app.logger.info("Log from flask/similar")
    request_bytes = 0
    product_id = int(request.args.get('id'))
    limit = int(request.args.get('limit'))
    data = {}
    data['Product'] = get_product(product_id)
    data['Reviews'] = get_review(product_id, limit)
    data['Similar'] = get_similar(product_id, limit)
    data = str(data)
    response = app.response_class(
        response=json.dumps(eval(data)),
        status=200,
        mimetype='application/json'
    )
    REQUEST_SIZE.observe(request_bytes)
    RESPONSE_SIZE.observe(len(data.encode('utf-8')))
    IN_PROGRESS.dec()
    return response
    # return Response(response,status='200',mimetype='application/json')


@app.route('/metrics/')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
