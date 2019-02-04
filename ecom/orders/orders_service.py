import json
import requests

from datetime import date, datetime
from decimal import Decimal
from flask import current_app
from postgres_db_handler import PostgresDBHandler
from sqlalchemy import Column, String, Integer, SmallInteger, Date, DateTime, Text, Numeric, func, desc
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class OrderItem(Base):
    __tablename__ = 'order_item'
    order_id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, primary_key=True)
    quantity = Column(SmallInteger)
    unit_price = Column(Numeric(8, 2))
    estimated_delivery_date = Column(Date)
    delivery_charges = Column(Numeric(8, 2))


class Order(Base):
    __tablename__ = 'customer_order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    order_date = Column(DateTime)
    payment_status = Column(String(20))
    delivery_address = Column(Text)


class OrdersServicer(object):
    # External dependencies
    PAYMENT_DETAILS_FORMAT = 'http://{payments_addr}/payment_details?order_id={order_id}'
    CHECK_AVAILABILITY_FORMAT = 'http://{inventory_addr}/fetch_availability?listing_ids={listing_ids}'
    # This can be moved to Products service
    # DELIVERY_ESTIMATE_FORMAT = 'http://{inventory_addr}/estimate_delivery?listing_ids={listing_ids}'
    LISTING_DETAILS = \
        'http://{inventory_addr}/fetch_details?listing_ids={listing_ids}&estimate_delivery=1&dest={dest_addr}'
    FETCH_CART_FORMAT = 'http://{cart_addr}/items?user_id={user_id}'

    def __init__(self, cart_addr: str, payments_addr: str, inventory_addr: str, db_handler: PostgresDBHandler):
        super().__init__()
        self.cart_addr = cart_addr
        self.payments_addr = payments_addr
        self.inventory_addr = inventory_addr
        self.db_handler = db_handler

    @staticmethod
    def __get_dictionary_for_order(order_rows):
        data = list()
        for order in order_rows:
            order_dict = dict()
            for k,v in order.__dict__.items():
                if not k.startswith('_'):
                    order_dict[k] = v
                    if isinstance(v, date) or isinstance(v, datetime):
                        order_dict[k] = v.isoformat()
            data.append(order_dict)
        return data

    @staticmethod
    def __get_dictionary_for_order_items(order_orderitem_rows):
        data = list()
        for order, order_item in order_orderitem_rows:
            order_item_dict = dict()
            for k,v in order_item.__dict__.items():
                if not k.startswith('_'):
                    order_item_dict[k] = v
                    if isinstance(v, date) or isinstance(v, datetime):
                        order_item_dict[k] = v.isoformat()
                    if isinstance(v, Decimal):
                        order_item_dict[k] = float(v)
            data.append(order_item_dict)
        return data

    def __get_payment_details(self, order_id):
        res = requests.get(url=self.PAYMENT_DETAILS_FORMAT.format(self.payments_addr, order_id=order_id))
        if res.status_code != 200:
            current_app.logger.warning("Could not fetch payment details")
            current_app.logger.warning("Status code: %d", res.status_code)
            if isinstance(res.reason, str):
                current_app.logger.warning("Reason: %s", res.reason)
            return None
        return json.loads(res.content)

    def __append_item_availability(self, cart):
        listing_ids = [str(item["listing_id"]) for item in cart]
        res = requests.get(url=self.CHECK_AVAILABILITY_FORMAT.format(inventory_addr=self.inventory_addr,
                                                                     listing_ids=','.join(listing_ids)))
        if res.status_code != 200:
            current_app.logger.error("Could not fetch availability")
            current_app.logger.error("Status code: %d", res.status_code)
            if isinstance(res.reason, str):
                current_app.logger.error("Reason: %s", res.reason)
            raise RuntimeError("Could not check availability. Please try again later")

        inventory_res = json.loads(res.content)
        items_to_delete = list()
        for item in cart:
            listing_id_str = str(item["listing_id"])
            if listing_id_str in inventory_res:
                item["available"] = int(inventory_res[listing_id_str])
            else:
                items_to_delete.append(item)

        for item in items_to_delete:
            cart.remove(item)

        return cart

    def __append_item_details(self, cart, dest_addr):
        listing_ids = [str(item["listing_id"]) for item in cart]
        res = requests.get(url=self.LISTING_DETAILS.format(inventory_addr=self.inventory_addr,
                                                           listing_ids=','.join(listing_ids),
                                                           dest_addr=dest_addr))
        if res.status_code != 200:
            current_app.logger.error("Could not fetch listing details")
            current_app.logger.error("Status code: %d", res.status_code)
            if isinstance(res.reason, str):
                current_app.logger.error("Reason: %s", res.reason)
            raise RuntimeError("Error confirming order price. Please try again later")

        inventory_res = json.loads(res.content)
        items_to_delete = list()
        for item in cart:
            listing_id_str = str(item["listing_id"])
            if listing_id_str in inventory_res:
                item["price"] = float(inventory_res[listing_id_str]["price"])
                item["estimated_delivery_date"] = inventory_res[listing_id_str]["estimated_delivery_date"]
                item["delivery_charges"] = float(inventory_res[listing_id_str]["delivery_charges"])
            else:
                items_to_delete.append(item)

        for item in items_to_delete:
            cart.remove(item)

        return cart

    def create_order(self, user_id: int, delivery_address: str):
        res = requests.get(url=self.FETCH_CART_FORMAT.format(cart_addr=self.cart_addr, user_id=user_id))
        if res.status_code != 200:
            current_app.logger.error("Could not fetch cart for user_id: %d", user_id)
            current_app.logger.error("Status code: %d", res.status_code)
            if isinstance(res.reason, str):
                current_app.logger.error("Reason: %s", res.reason)
            raise RuntimeError("Could not fetch cart for user_id: %d" % user_id)
        cart_res = json.loads(res.content)
        if len(cart_res["cart"]) == 0:
            raise ValueError("Cart is empty for user_id: %d" % user_id)

        cart = cart_res["cart"]
        cart = self.__append_item_availability(cart=cart)
        for item in cart:
            if item["quantity"] > item["available"]:
                raise ValueError("Not enough quantity available for item: %d", item["listing_id"])
        cart = self.__append_item_details(cart=cart, dest_addr=delivery_address)
        db_session = self.db_handler.getSession()
        try:
            order = Order(user_id=user_id, order_date=func.now(), payment_status="Pending",
                          delivery_address=delivery_address)
            db_session.add(order)
            # Run flush to fetch the order id which is a serial
            db_session.flush()
            for item in cart:
                order_item = OrderItem(order_id=order.id, listing_id=item["listing_id"], quantity=item["quantity"],
                                       unit_price=item["price"],
                                       estimated_delivery_date=item["estimated_delivery_date"],
                                       delivery_charges=item["delivery_charges"])
                db_session.add(order_item)
            response = self.__get_dictionary_for_order(order_rows=[order])[0]
            db_session.commit()
            return response
        except:
            db_session.rollback()
            current_app.logger.exception("Error creating order for user_id: %d", user_id)
            raise RuntimeError("Error creating order, please try again")
        finally:
            db_session.close()

    def get_order_details(self, order_id: int):
        db_session = self.db_handler.getSession()
        try:
            order_details = db_session.query(Order, OrderItem).\
                filter(Order.id == OrderItem.order_id,
                       Order.id == order_id).all()
            if order_details is None or len(order_details) == 0:
                raise ValueError("Invalid order id: %d", order_id)
            payment_details = dict()
            order = order_details[0][0]
            order_dict = self.__get_dictionary_for_order(order_rows=[order])[0]
            if order.payment_status != "Pending":
                order_dict["payment_details"] = self.__get_payment_details(order_id=order_id)
            order_item_dicts = self.__get_dictionary_for_order_items(order_orderitem_rows=order_details)
            order_dict["items"] = order_item_dicts
            return order_dict
        finally:
            db_session.close()

    def list_orders_for_user(self, user_id, limit):
        db_session = self.db_handler.getSession()
        try:
            orders = db_session.query(Order).filter(Order.user_id == user_id).\
                order_by(desc(Order.order_date)).\
                limit(limit)
            return self.__get_dictionary_for_order(order_rows=orders)
        finally:
            db_session.close()

    def update_payment_status(self, order_id, payment_status):
        db_session = self.db_handler.getSession()
        try:
            order = db_session.query(Order).filter(Order.id == order_id).first()
            if order is None:
                current_app.logger.warning("Order id %d does not exist", order_id)
                raise ValueError("Order id %d does not exist", order_id)
            order.payment_status = payment_status
            db_session.merge(order)
            db_session.commit()
            return dict(id=order.id, payment_status=order.payment_status)
        finally:
            db_session.close()
