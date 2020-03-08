from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)

    def __init__(
            self,
            name,
            surname,
            email,
            phone):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
