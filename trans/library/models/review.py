import enum

from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Enum,
    ForeignKey
)
from sqlalchemy.orm import (
    relationship,
    backref
)
from datetime import datetime


class Rating(enum.Enum):
    NEGATIVE = 1
    NEUTRAL = 2
    POSITIVE = 3


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    rating = Column(Enum(Rating))
    review = Column(String)
    company_id = Column(Integer)
    user_id = Column(Integer)

    def __init__(
            self,
            rating,
            review,
            company_id,
            user_id):
        self.rating = Rating(int(rating))
        self.review = review
        self.company_id = company_id
        self.user_id = user_id
