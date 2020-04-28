import os
import re
import sqlalchemy

from datetime import datetime
from sqlalchemy import (
    and_,
    or_
)
from library.database import get_session
from library.models.car import Car
from library.models.user import User
from library.models.goods import Goods
from library.models.company import Company
from library.models.review import Review


DEFAULT_CONFIG_DIRECTORY = os.path.expanduser("~/Documents/Диплом/.trans/")
DEFAULT_DATABASE_URL = ''.join(["sqlite:///",
                                DEFAULT_CONFIG_DIRECTORY,
                                "trans.db"])


class API:
    def __init__(self, connection_string):
        self._session = get_session(connection_string)

    def create_car(
            self,
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

        car = Car(
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
            note,
            urgently
        )

        self._add(car)

        return car.id

    def get_car(self, car_id):
        try:
            return (self._session.query(Car)
                    .filter(Car.id == car_id).one())
        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Car not found")

    def edit_car(
            self,
            car_id,
            body_type=None,
            download_type=None,
            carrying_capacity=None,
            volume=None,
            loading_date_from=None,
            loading_date_by=None,
            country_loading=None,
            city_loading=None,
            country_unloading=None,
            city_unloading=None,
            note=None,
            urgently=None):
        car = self.get_car(car_id)

        if body_type is not None:
            car.body_type = body_type

        if download_type is not None:
            car.download_type = download_type

        if carrying_capacity is not None:
            car.carrying_capacity = carrying_capacity

        if volume is not None:
            car.volume = volume

        if loading_date_from is not None:
            car.loading_date_from = loading_date_from

        if loading_date_by is not None:
            car.loading_date_by = loading_date_by

        if country_loading is not None:
            car.city_loading = city_loading

        if country_unloading is not None:
            car.country_unloading = country_unloading

        if city_unloading is not None:
            car.city_unloading = city_unloading

        if note is not None:
            car.note = note

        if urgently is not None:
            car.urgently = urgently

        self._session.commit()

    def delete_car(self, car_id):
        car = self.get_car(car_id)

        self._delete(car)

    def create_user(
            self,
            nickname,
            name,
            surname,
            email,
            phone):

        user = User(
            nickname,
            name,
            surname,
            email,
            phone
        )

        self._add(user)

        return user.id

    def get_user(self, user_id=None, nickname=None):
        _filter = and_(
            or_(user_id is None, User.id == user_id),
            or_(nickname is None, User.nickname == nickname)
        )

        try:
            return (self._session.query(User)
                .filter(_filter).one_or_none())

        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("User not found")

    def edit_user(
            self,
            nickname,
            name=None,
            surname=None,
            email=None,
            phone=None):
        user = self.get_user(nickname=nickname)

        if name is not None:
            user.name = name

        if surname is not None:
            user.surname = surname

        if email is not None:
            user.email = email

        if phone is not None:
            user.phone = phone

        self._session.commit()

    def delete_user(self, nickname):
        user = self.get_user(nickname=nickname)

        self._delete(user)

    def create_goods(
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

        goods = Goods(
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
            note,
            urgently
        )

        self._add(goods)

        return goods.id

    def get_goods(self, goods_id):
        try:
            return (self._session.query(Goods)
                    .filter(Goods.id == goods_id).one())
        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Goods not found")

    def edit_goods(
            self,
            goods_id,
            name=None,
            body_type=None,
            weigh=None,
            volume=None,
            loading_date_from=None,
            loading_date_by=None,
            country_loading=None,
            city_loading=None,
            country_unloading=None,
            city_unloading=None,
            note=None,
            urgently=None):

        goods = self.get_goods(goods_id)

        if name is not None:
            goods.name = name

        if body_type is not None:
            goods.body_type = body_type

        if weigh is not None:
            goods.weigh = weigh

        if volume is not None:
            goods.volume = volume

        if loading_date_from is not None:
            goods.loading_date_from = loading_date_from

        if loading_date_by is not None:
            goods.loading_date_by = loading_date_by

        if country_loading is not None:
            goods.city_loading = city_loading

        if country_unloading is not None:
            goods.country_unloading = country_unloading

        if city_unloading is not None:
            goods.city_unloading = city_unloading

        if note is not None:
            goods.note = note

        if urgently is not None:
            goods.urgently = urgently

        self._session.commit()

    def delete_goods(self, goods_id):
        goods = self.get_goods(goods_id)

        self._delete(goods)

    def create_company(
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

        company = Company(
            nickname,
            UNP,
            name,
            primary_occupation,
            license,
            country,
            town,
            address,
            phone,
            description
        )

        self._add(company)

        return company.id

    def get_company(self, company_id=None, nickname=None):
        try:
            if nickname is not None:
                return (self._session.query(Company)
                    .filter(Company.nickname == nickname).one_or_none())
            else:
                return (self._session.query(Company)
                        .filter(Company.id == company_id).one())
        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Company not found")

    def get_companys(self, primary_occupation=None, name=None, country=None):
        _filter = and_(
            or_(name is None, Company.name == name),
            or_(primary_occupation is None, Company.primary_occupation == primary_occupation),
            or_(country is None, Company.country == country)
        )

        companys = self._session.query(Company).filter(_filter).all()
        self._session.commit()

        return companys

    def edit_company(
            self,
            nickname,
            UNP=None,
            name=None,
            primary_occupation=None,
            license=None,
            country=None,
            town=None,
            address=None,
            phone=None,
            description=None):
        company = self.get_company(nickname=nickname)

        if UNP is not None:
            company.UNP = UNP

        if name is not None:
            company.name = name

        if primary_occupation is not None:
            company.primary_occupation = primary_occupation

        if license is not None:
            company.license = license

        if country is not None:
            company.country = country

        if town is not None:
            company.town = town

        if address is not None:
            company.address = address

        if phone is not None:
            company.phone = phone

        if description is not None:
            company.description = description
            company.small_description = company.pars_description()

        self._session.commit()

    def delete_company(self, company_id):
        company = self.get_company(company_id=company_id)

        self._delete(company)

    def _add(self, object):
        self._session.add(object)
        self._session.commit()

    def _delete(self, object):
        self._session.delete(object)
        self._session.commit()

    def create_review(
            self,
            rating,
            review,
            company_id,
            user_id):

        review = Review(
            rating,
            review,
            company_id,
            user_id
        )

        self._add(review)

        return review.id

    def get_reviews(self, company_id):
        try:
            return (self._session.query(Review)
                .filter(Review.company_id == company_id).all())

        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Review not found")

    def get_company_rating(self, company_id):
        company = self.get_reviews(company_id)

    