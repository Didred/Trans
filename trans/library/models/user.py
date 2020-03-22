from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)

    def __init__(
            self,
            nickname,
            name,
            surname,
            email,
            phone):
        self.nickname = nickname
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
