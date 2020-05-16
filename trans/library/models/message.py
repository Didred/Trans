from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime
)
import datetime


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer)
    recipient_id = Column(Integer)
    text = Column(String)
    date = Column(DateTime)

    def __init__(
            self,
            sender_id,
            recipient_id,
            text):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.text = text
        self.date = datetime.datetime.now() + datetime.timedelta(hours=3)
