import enum

from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Enum,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import (
    relationship,
    backref
)
from datetime import datetime


class Status(enum.Enum):
    WAITING = 1
    ACCEPTED = 2
    REJECTED = 3


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    car_id = Column(Integer)
    goods_id = Column(Integer)
    status = Column(Enum(Status))
    date_create = Column(DateTime)
    date = Column(DateTime)

    def __init__(
            self,
            user_id,
            car_id,
            goods_id,
            date_create):
        self.user_id = user_id
        self.car_id = car_id
        self.goods_id = goods_id
        self.status = Status(1)
        self.date_create = date_create
