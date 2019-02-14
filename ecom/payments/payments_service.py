import json
import base64
import requests

from decimal import Decimal
from datetime import date
from flask import current_app
from postgres_db_handler import PostgresDBHandler
from sqlalchemy import Column, String, Integer, DateTime, Text, Numeric, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    payment_mode = Column(String(50))
    mode_details = Column(Text)
    amount = Column(Numeric(8, 2))
    status = Column(String(20))
    error_details = Column(Text)
    transaction_date = Column(DateTime)


class PaymentsServicer(object):
    JSON_COLUMNS = ["mode_details"]

    # External dependencies
    UPDATE_PAYMENT_STATUS_FORMAT = 'http://{orders_addr}/update_payment_status?id={order_id}&status={status}'

    def __init__(self, orders_addr: str, db_handler: PostgresDBHandler):
        super().__init__()
        self.orders_addr = orders_addr
        self.db_handler = db_handler

    def __get_payment_dict(self, payment):
        payment_dict = dict()
        for k, v in payment.__dict__.items():
            if not k.startswith('_'):
                payment_dict[k] = v
                if isinstance(v, Decimal):
                    payment_dict[k] = float(v)
                if isinstance(v, date):
                    payment_dict[k] = v.isoformat()
                if k in self.JSON_COLUMNS:
                    payment_dict[k] = json.loads(v)
        return payment_dict

    def __update_payment_status_on_order(self, order_id: int, status: str):
        res = requests.put(url=self.UPDATE_PAYMENT_STATUS_FORMAT.format(orders_addr=self.orders_addr, order_id=order_id,
                                                                        status=status))
        return res.status_code == 200

    def initiate_payment(self, order_id, mode, mode_details, amount):
        db_session = self.db_handler.getSession()
        try:
            response = dict(acknowledge=True)
            payment = Payment(order_id=order_id, payment_mode=mode, mode_details=json.dumps(mode_details),
                              amount=amount, transaction_date=func.now())
            payment.status = "Created"
            db_session.add(payment)
            db_session.commit()
            res = requests.get(url='http://www.declayer.com')
            if res.status_code != 200:
                current_app.logger.error("Error initiating payment::")
                current_app.logger.error("Status code: %d", res.status_code)
                if isinstance(res.reason, str):
                    current_app.logger.error("Reason: %s", res.reason)
                payment.status = "Terminated"
                response["acknowledge"] = False
            else:
                payment.status = "Initiated"
            db_session.merge(payment)
            db_session.commit()
            return response
        finally:
            db_session.close()

    def get_payment(self, order_id: int):
        db_session = self.db_handler.getSession()
        try:
            payment = db_session.query(Payment).filter(Payment.order_id == order_id).first()
            if payment is None:
                current_app.logger.warning("Payment details not found for order id: %d", order_id)
                return dict()
            return self.__get_payment_dict(payment=payment)
        finally:
            db_session.close()

    def handle_payment_callback(self, payment_id: int, success: bool, error_details: str):
        db_session = self.db_handler.getSession()
        try:
            payment = db_session.query(Payment).filter(Payment.id == payment_id).first()
            if payment is None:
                # We can't return an error to the callback so don't throw an exception, just log error
                current_app.logger.error("Payment callback received with invalid id: %d", payment_id)
            else:
                payment.status = "Success" if success else "Failed"
                if not success:
                    payment.error_details = error_details
                db_session.merge(payment)
                # Notify ordering system
                notify_success = self.__update_payment_status_on_order(order_id=payment.order_id,
                                                                       status=payment.status)
                if not notify_success:
                    current_app.logger.error("Error updating payment status in Order system")
                db_session.commit()
        finally:
            db_session.close()
