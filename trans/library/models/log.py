from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime
)


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    username = Column(String)
    date = Column(DateTime)
    text = Column(String)

    def __init__(
            self,
            company_id,
            username,
            date,
            text):
        self.company_id = company_id
        self.username = username
        self.date = date
        self.text = text
