from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer
)


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    UNP = Column(String) #?
    name = Column(String)
    primary_occupation = Column(String)
    country = Column(String)
    town = Column(String)
    address = Column(String)
    phone = Column(String)

    def __init__(
            self,
            UNP,
            name,
            primary_occupation,
            country,
            town,
            address,
            phone):
        self.UNP = UNP
        self.name = name
        self.primary_occupation = primary_occupation
        self.country = country
        self.town = town
        self.address = address
        self.phone = phone
