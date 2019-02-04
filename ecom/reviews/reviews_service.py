import json

from datetime import date
from flask import current_app
from postgres_db_handler import PostgresDBHandler
from sqlalchemy import Column, String, Integer, SmallInteger, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    model_number = Column(String(100))
    rating = Column(SmallInteger)
    review_text = Column(Text)
    review_date = Column(DateTime)


class ReviewsServicer(object):
    def __init__(self, db_handler: PostgresDBHandler):
        super().__init__()
        self.db_handler = db_handler

    def __get_review_dict(self, review_objects):
        reviews = list()
        for review in review_objects:
            review_dict = dict()
            for k,v in review.__dict__.items():
                if not k.startswith('_'):
                    review_dict[k] = v
                    if isinstance(v, date):
                        review_dict[k] = v.isoformat()
            reviews.append(review_dict)
        return reviews

    def get_reviews(self, model_number: int, limit: int):
        current_app.logger.debug("Fetching reviews for product id: %s" % model_number)
        db_session = self.db_handler.getSession()
        try:
            reviews = db_session.query(Review).filter(
                Review.model_number == model_number).limit(limit).all()
            return self.__get_review_dict(review_objects=reviews)
        finally:
            db_session.close()

    def get_review(self, review_id: int):
        current_app.logger.debug("Fetching review id: %s" % review_id)
        db_session = self.db_handler.getSession()
        try:
            review = db_session.query(Review).filter(
                Review.id == review_id).first()
            if review is None:
                raise ValueError("Invalid review id: %d" % review_id)
            return self.__get_review_dict(review_objects=[review])
        finally:
            db_session.close()

    def save_review(self, review_json):
        review = Review(**review_json)
        db_session = self.db_handler.getSession()
        try:
            if review.id is None:
                db_session.add(review)
            else:
                db_session.merge(review)
            db_session.commit()
            return review.id
        finally:
            db_session.close()

    def get_avg_rating(self, model_number):
        db_session = self.db_handler.getSession()
        try:
            avg_rating = db_session.query(func.avg(Review.rating)).filter(Review.model_number == model_number).first()
            if avg_rating is None or len(avg_rating) == 0:
                avg_rating = -1
            return float(avg_rating[0])
        finally:
            db_session.close()
