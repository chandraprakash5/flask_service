import json
import random

from datetime import date, datetime, timedelta
from decimal import Decimal
from flask import current_app
from postgres_db_handler import PostgresDBHandler
from sqlalchemy import Column, String, Integer, SmallInteger, Numeric
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Listing(Base):
    __tablename__ = 'listing'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    seller_id = Column(Integer)
    location = Column(String(100))
    price = Column(Numeric(8, 2))
    quantity = Column(SmallInteger)


class InventoryServicer(object):
    def __init__(self, db_handler: PostgresDBHandler):
        super().__init__()
        self.db_handler = db_handler

    def __get_listings_dict(self, listing_objects):
        listings = list()
        for listing in listing_objects:
            listing_dict = dict()
            for k,v in listing.__dict__.items():
                if not k.startswith('_'):
                    listing_dict[k] = v
                    if isinstance(v, date) or isinstance(v, datetime):
                        listing_dict[k] = v.isoformat()
                    if isinstance(v, Decimal):
                        listing_dict[k] = float(v)
            listings.append(listing_dict)
        return listings

    def __estimate_delivery(self, item_addr: str, dest_addr: str):
        current_app.logger.debug("Estimating delivery time from %s to %s", item_addr, dest_addr)
        delivery_days = random.randint(1, 10)
        delivery_charges = 0 if delivery_days < 3 else 99
        return delivery_days, delivery_charges

    def get_listings_for_product(self, product_id: int, limit: int):
        current_app.logger.debug("Fetching listings for product id: %s" % product_id)
        db_session = self.db_handler.getSession()
        try:
            listings = db_session.query(Listing).filter(
                Listing.product_id == product_id).limit(limit).all()
            return self.__get_listings_dict(listing_objects=listings)
        finally:
            db_session.close()

    def get_availability(self, listing_ids: list):
        current_app.logger.debug("Fetching listing ids: %s", listing_ids)
        db_session = self.db_handler.getSession()
        try:
            listing_objs = db_session.query(Listing.id, Listing.quantity).\
                filter(Listing.id.in_(listing_ids)).all()
            if len(listing_objs) != len(listing_ids):
                fetched_ids = set([listing.id for listing in listing_objs])
                sent_ids = set(listing_ids)
                missing_ids = list(sent_ids - fetched_ids)
                current_app.logger.warning("Invalid listing ids: %s", missing_ids)
                raise ValueError("Invalid listing ids: %s" % missing_ids)

            listing_availability = dict()
            for listing in listing_objs:
                listing_availability[listing.id] = listing.quantity
            return listing_availability
        finally:
            db_session.close()

    def get_listing_details(self, listing_ids: list, estimate_delivery: bool, dest_addr: str):
        current_app.logger.debug("Fetching listing ids: %s", listing_ids)
        db_session = self.db_handler.getSession()
        try:
            listing_objs = db_session.query(Listing).filter(Listing.id.in_(listing_ids)).all()
            if len(listing_objs) != len(listing_ids):
                fetched_ids = set([listing.id for listing in listing_objs])
                sent_ids = set(listing_ids)
                missing_ids = list(sent_ids - fetched_ids)
                current_app.logger.warning("Invalid listing ids: %s" % missing_ids)
                raise ValueError("Invalid listing ids: %s" % missing_ids)

            listings = self.__get_listings_dict(listing_objects=listing_objs)
            if estimate_delivery:
                for listing in listings:
                    delivery_days, delivery_charges = self.__estimate_delivery(item_addr=listing["location"],
                                                                               dest_addr=dest_addr)
                    estimated_delivery_date = date.today() + timedelta(days=delivery_days)
                    listing['estimated_delivery_date'] = estimated_delivery_date.isoformat()
                    listing['delivery_charges'] = delivery_charges
            return {listing["id"]: listing for listing in listings}
        finally:
            db_session.close()
