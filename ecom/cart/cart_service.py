import json
import redis

from flask import current_app


class Cart(object):
    class CartItem(object):
        def __init__(self, listing_id, quantity):
            self.listing_id = listing_id
            self.quantity = quantity

        def __repr__(self):
            return "CartItem :: {listing_id}::{quantity}".format(listing_id=self.listing_id, quantity=self.quantity)

    def __init__(self):
        self.items = list()

    def add_item(self, listing_id):
        existing_item = [item for item in self.items if item.listing_id == listing_id]
        if len(existing_item) > 0:
            item = existing_item[0]
            item.quantity += 1
        else:
            self.items.append(Cart.CartItem(listing_id=listing_id, quantity=1))

    def remove_item(self, listing_id):
        existing_item = [item for item in self.items if item.listing_id == listing_id]
        if len(existing_item) > 0:
            item = existing_item[0]
            item.quantity -= 1
            if item.quantity == 0:
                self.items.remove(item)
        else:
            raise ValueError("Item with listing_id %d not found in cart", listing_id)

    def is_empty(self):
        return len(self.items) == 0

    def to_json(self):
        item_list = [item.__dict__ for item in self.items]
        return json.dumps(dict(cart=item_list))

    @classmethod
    def from_json(cls, json_str):
        cart = cls()
        cart.items = [Cart.CartItem(**item) for item in json.loads(json_str)["cart"]]
        return cart


class CartServicer(object):
    def __init__(self, redis_host: str, redis_port: int):
        super().__init__()
        self.redis_db = redis.Redis(host=redis_host, port=redis_port)

    def __get_cart_key_for_user(self, user_id):
        cart_key = 'user-{user_id}'.format(user_id=user_id)
        return cart_key

    def add_item_to_cart(self, user_id: int, listing_id: int):
        cart_key = self.__get_cart_key_for_user(user_id=user_id)
        user_cart_json = self.redis_db.get(cart_key)
        user_cart = Cart.from_json(json_str=user_cart_json) if user_cart_json else Cart()
        user_cart.add_item(listing_id=listing_id)
        user_cart_json = user_cart.to_json()
        self.redis_db.set(cart_key, user_cart_json)
        return user_cart_json

    def remove_item_to_cart(self, user_id: int, listing_id: int):
        cart_key = self.__get_cart_key_for_user(user_id=user_id)
        user_cart_json = self.redis_db.get(cart_key)
        user_cart = Cart.from_json(json_str=user_cart_json) if user_cart_json else Cart()
        user_cart.remove_item(listing_id=listing_id)
        user_cart_json = user_cart.to_json()
        if not user_cart.is_empty():
            self.redis_db.set(cart_key, user_cart_json)
        else:
            self.redis_db.delete(cart_key)
            current_app.logger.info("Cart is now empty for user: %d", user_id)
        return user_cart_json

    def list_items_in_cart(self, user_id: int):
        cart_key = self.__get_cart_key_for_user(user_id=user_id)
        user_cart_json = self.redis_db.get(cart_key)
        if user_cart_json is None:
            cart = Cart()
            user_cart_json = cart.to_json()
        return user_cart_json

    def clear_cart(self, user_id):
        cart_key = self.__get_cart_key_for_user(user_id=user_id)
        if self.redis_db.exists(cart_key):
            self.redis_db.delete(cart_key)
        current_app.logger.info("Cart has been cleared for user: %d", user_id)
        cart = Cart()
        return cart.to_json()
