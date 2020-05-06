import enum

from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    Enum
)
from sqlalchemy.orm import (
    relationship,
    backref
)


class Role(enum.Enum):
    USER = 1
    ADMINISTRATOR = 2
    MODERATOR = 3
    ADMIN = 4


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)
    company_id = Column(Integer)
    role = Column(Enum(Role))

    def __init__(
            self,
            nickname,
            name,
            surname,
            email,
            phone,
            company_id,
            role):
        self.nickname = nickname
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.company_id = company_id
        self.role = role

    def add_company(self, company_id):
        self.company_id = company_id

    def remove_company(self):
        self.role = Role(1)
        self.company_id = None