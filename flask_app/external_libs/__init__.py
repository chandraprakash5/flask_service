import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from .base_pb2 import ProductId, Limit, UserId
from .products_pb2 import Product, ReviewedProduct
from .products_pb2_grpc import ProductsStub
from .reviews_pb2 import Review, ReviewsRequest, ReviewId
from .reviews_pb2_grpc import ReviewsStub
from .similar_pb2 import SimilarProductRequest
from .similar_pb2_grpc import SimilarProductsStub