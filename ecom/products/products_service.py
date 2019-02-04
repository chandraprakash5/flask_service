import json

from datetime import date
from flask import current_app
from postgres_db_handler import PostgresDBHandler
from requests import get as requests_get
from sqlalchemy import Column, String, Integer, SmallInteger, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    model_number = Column(String(100))
    title = Column(String(250))
    description = Column(Text)
    brand_name = Column(String(100))
    variant = Column(Text)
    details = Column(Text)


class ProductsServicer(object):
    """Provides methods that implement functionality of products server."""

    JSON_COLUMNS = ["variant", "details"]

    # External dependencies
    AVG_RATING_FORMAT = 'http://{reviews_addr}/rating?model_number={model_number}'
    FETCH_LISTINGS_FORMAT = 'http://{inventory_addr}/listings?product_id={product_id}'

    def __init__(self, reviews_addr: str, inventory_addr: str, db_handler: PostgresDBHandler):
        super().__init__()
        self.reviews_addr= reviews_addr
        self.inventory_addr = inventory_addr
        self.db_handler = db_handler

    def __get_avg_rating_for_product_id(self, model_number):
        try:
            res = requests_get(url=self.AVG_RATING_FORMAT.format(reviews_addr=self.reviews_addr,
                                                                 model_number=model_number))
            if res.status_code != 200:
                current_app.logger.warning("Could not fetch rating for product id: %s", model_number)
                return -1
            data = json.loads(res.content)
            return data["rating"]
        except Exception as e:
            current_app.logger.exception("Error fetching rating for product id: %s", model_number)
            return -1

    def __fetch_listings_for_product(self, product_id):
        try:
            res = requests_get(url=self.FETCH_LISTINGS_FORMAT.format(inventory_addr=self.inventory_addr,
                                                                     product_id=product_id))
            if res.status_code != 200:
                current_app.logger.warning("Could not fetch rating for product id: %d", product_id)
                return -1
            data = json.loads(res.content)
            return data
        except Exception as e:
            current_app.logger.exception("Error fetching listings for product id: %d", product_id)
            return []

    def __get_product_dict(self, products, fetch_avg_rating, fetch_listings):
        data = list()
        for product in products:
            product_dict = dict()
            for k,v in product.__dict__.items():
                if not k.startswith('_'):
                    product_dict[k] = v
                    if isinstance(v, date):
                        product_dict[k] = v.isoformat()
                    if k in self.JSON_COLUMNS:
                        product_dict[k] = json.loads(v)
            if fetch_avg_rating:
                product_dict["rating"] = self.__get_avg_rating_for_product_id(model_number=product_dict["model_number"])
            if fetch_listings:
                product_dict["listings"] = self.__fetch_listings_for_product(product_id=product_dict["id"])
            data.append(product_dict)
        return data

    def get_product(self, product_id: int):
        db_session = self.db_handler.getSession()
        try:
            product = db_session.query(Product).filter(Product.id == product_id).first()
            if product is None:
                current_app.logger.error("Invalid product id: %d", product_id)
                raise ValueError("Invalid product id: %d" % product_id)
            product_dict = self.__get_product_dict(products=[product], fetch_avg_rating=True, fetch_listings=True)
            return product_dict[0]
        finally:
            db_session.close()

    def list_products(self, limit: int) -> list:
        db_session = self.db_handler.getSession()
        try:
            products = db_session.query(Product).limit(limit).all()
            response_data = self.__get_product_dict(products=products, fetch_avg_rating=True, fetch_listings=False)
            current_app.logger.debug("Returning {count} products".format(count=len(response_data)))
            for product in response_data:
                yield product
        finally:
            db_session.close()
