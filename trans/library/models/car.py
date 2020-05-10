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
    city_loading = Column(String)
    country_unloading = Column(String)
    city_unloading = Column(String)
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
            city_loading,
            country_unloading,
            city_unloading,
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
        self.city_loading = city_loading
        self.country_unloading = country_unloading
        self.city_unloading = city_unloading
        self.note = note if note is not None else None
        self.urgently = True if urgently is not None else False

    def __str__(self):
        result = "\nТип кузова: %s\n" % self.body_type
        result += "Тип загрузки: "

        for i in self.download_type:
            result += i + ", "
        result = result[:-2] + "\n"

        result += "Грузоподъемность, т.: %d\n" % self.carrying_capacity
        result += "Объем, м3: %d\n" % self.volume
        result += "Дата готовности транспорта к загрузке: c %s по %s\n" % (self.loading_date_from, self.loading_date_by) # заменить на объект
        result += "Место загрузки (страна): %s\n" % self.country_loading
        result += "Место загрузки (город): %s\n" % self.city_loading
        result += "Место разгрузки (страна): %s\n" % self.country_unloading
        result += "Место разгрузки (город): %s\n" % self.city_unloading
        if self.note is not None:
            result += "Примечания: %s\n" % self.note
        if self.urgently is not None:
            result += "Срочно!"

        return result
