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
    name = Column(String)
    body_type = Column(String)
    weigh = Column(String)
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
            name,
            body_type,
            weigh,
            volume,
            loading_date_from,
            loading_date_by,
            country_loading,
            city_loading,
            country_unloading,
            city_unloading,
            note=None,
            urgently=None):
        self.name = name
        self.body_type = body_type
        self.weigh = weigh
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
        result = "\nНаименование груза: %s\n" % self.name
        result += "Тип кузова: %s\n" % self.body_type
        result += "Вес, т: %d\n" % self.weigh
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


goods = Goods("Молоко", "Тент", 200, 10, "04.03.2020", "05.03.2020", "Беларусь", "Минск", "Россия", "Москва", "Примечание!", urgently=True)
print(goods)



