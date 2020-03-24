from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime
)
from datetime import datetime


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    UNP = Column(String) #?
    name = Column(String)
    primary_occupation = Column(String)
    license = Column(String)
    country = Column(String)
    town = Column(String)
    address = Column(String)
    phone = Column(String)
    date_registration = Column(DateTime)
    description = Column(String)
    small_description = Column(String)

    def __init__(
            self,
            nickname,
            UNP,
            name,
            primary_occupation,
            license,
            country,
            town,
            address,
            phone,
            description):
        self.nickname = nickname
        self.UNP = UNP
        self.name = name
        self.primary_occupation = primary_occupation
        self.license = license
        self.country = country
        self.town = town
        self.address = address
        self.phone = phone
        self.date_registration = datetime.now()
        self.description = description
        self.small_description = self._pars_description()

    def pars_description(self):
        small_description = self.description[0:420]
        residue = self.description[420:]

        index = residue.index(" ")
        small_description += residue[0: index] + " ..."

        return small_description
