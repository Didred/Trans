from library.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean
)


class Goods(Base):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    body_type = Column(String)
    car_count = Column(Integer)
    download_type = Column(String)
    belt_count = Column(Integer)
    weigh = Column(Integer)
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
            user_id,
            name,
            body_type,
            car_count,
            download_type,
            belt_count,
            weigh,
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
        self.user_id = user_id
        self.name = name
        self.body_type = body_type
        self.car_count = car_count
        self.download_type = download_type
        self.belt_count = belt_count
        self.weigh = weigh
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