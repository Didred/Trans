from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean
)


class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    body_type = Column(String)
    download_type = Column(String) #?
    carrying_capacity = Column(Integer)
    volume = Column(Integer)
    loading_date_from = Column(DateTime)
    loading_date_by = Column(DateTime)
    country_loading = Column(String)
    country_unloading = Column(String)
    rate = Column(Integer)
    price = Column(String)
    form_price = Column(String)
    note = Column(String)
    urgently = Column(Boolean)

    def __init__(
            self,
            company_id,
            body_type,
            download_type,
            carrying_capacity,
            volume,
            loading_date_from,
            loading_date_by,
            country_loading,
            country_unloading,
            rate,
            price,
            form_price,
            note=None,
            urgently=None):
        self.company_id = company_id
        self.body_type = body_type
        self.download_type = download_type
        self.carrying_capacity = carrying_capacity
        self.volume = volume
        self.loading_date_from = loading_date_from
        self.loading_date_by = loading_date_by
        self.country_loading = country_loading
        self.country_unloading = country_unloading
        self.rate = rate
        self.price = price
        self.form_price = form_price
        self.note = note if note is not None else None
        self.urgently = True if urgently is not None else False

    def get_date(self):
        return self.loading_date_from.strftime("%d.%m.%Y") + " - " + self.loading_date_by.strftime("%d.%m.%Y")
