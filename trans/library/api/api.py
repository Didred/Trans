import os
import re
import sqlalchemy
import imgurpython
import pytz

import datetime
from sqlalchemy import (
    and_,
    or_
)
from library.database import get_session
from library.models.car import Car
from library.models.user import User, Role
from library.models.goods import Goods
from library.models.company import Company
from library.models.review import Review, Rating
from library.models.log import Log
from library.models.message import Message
from library.models.request import Request, Status
from sources.templates import (
    RAISING_TO_ADMINISTRATOR,
    LOWERING_FROM_ADMINISTRATOR,
    REMOVE_EMPLOYEE,
    ADD_EMPLOYEE,
    CREATE_CAR,
    REMOVE_CAR,
    ACCEPT_REQUEST,
    REJECT_REQUEST
)


DEFAULT_CONFIG_DIRECTORY = os.path.expanduser("~/Documents/Диплом/.trans/")
DEFAULT_DATABASE_URL = ''.join(["sqlite:///",
                                DEFAULT_CONFIG_DIRECTORY,
                                "trans.db"])
CLIENT_ID = "d67dc6e4d99cc43"
CLIENT_SECRET = "9c8ac0ca9381ac32be63715b26dbd5d8db52911e"


class API:
    def __init__(self, connection_string):
        self._session = get_session(connection_string)

    def create_car(
            self,
            administrator_nickname,
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
        administrator = self.get_user(nickname=administrator_nickname)

        if administrator.role.value > 1 and administrator.company_id == company_id:
            car = Car(
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
                note=note,
                urgently=urgently
            )

            self._add(car)

            text_log = CREATE_CAR
            self.create_log(company_id, administrator_nickname, text_log, "машину", car.id)

            return car.id

    def get_car(self, car_id):
        try:
            return (self._session.query(Car)
                    .filter(Car.id == car_id).one_or_none())
        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Car not found")

    def get_cars(self,
            body_type=None,
            download_type=None,
            carrying_capacity_min=None,
            carrying_capacity_max=None,
            volume_min=None,
            volume_max=None,
            loading_date_from=None,
            loading_date_by=None,
            country_loading=None,
            country_unloading=None,
            company_id=None):
        if body_type and int(body_type) == -1:
            body_type = None

        if download_type and int(download_type) == -1:
            download_type = None

        if not country_loading:
            country_loading = None

        if not country_unloading:
            country_unloading = None

        _filter = and_(
            or_(body_type is None, Car.body_type == body_type),
            or_(download_type is None, Car.download_type == download_type),
            or_(country_loading is None, Car.country_loading == country_loading),
            or_(country_unloading is None, Car.country_unloading == country_unloading),
            or_(company_id is None, Car.company_id == company_id)
        )

        cars = self._session.query(Car).filter(_filter).all()
        self._session.commit()

        result_cars = []

        for car in cars:
            if carrying_capacity_min:
                if car.carrying_capacity >= int(carrying_capacity_min):
                    result_cars.append(car)
            else:
                result_cars.append(car)

        cars = result_cars.copy()
        result_cars = []
        for car in cars:
            if carrying_capacity_max:
                if car.carrying_capacity <= int(carrying_capacity_max):
                    result_cars.append(car)
            else:
                result_cars.append(car)

        cars = result_cars.copy()
        result_cars = []
        for car in cars:
            if volume_min:
                if car.volume >= int(volume_min):
                    result_cars.append(car)
            else:
                result_cars.append(car)

        cars = result_cars.copy()
        result_cars = []
        for car in cars:
            if volume_max:
                if car.volume <= int(volume_max):
                    result_cars.append(car)
            else:
                result_cars.append(car)

        utc=pytz.UTC
        cars = result_cars.copy()
        result_cars = []
        for car in cars:
            if loading_date_from:
                if car.loading_date_from.replace(tzinfo=utc) >= loading_date_from:
                    result_cars.append(car)
            else:
                result_cars.append(car)

        cars = result_cars.copy()
        result_cars = []
        for car in cars:
            if loading_date_by:
                if car.loading_date_by.replace(tzinfo=utc) <= loading_date_by:
                    result_cars.append(car)
            else:
                result_cars.append(car)

        return result_cars


    def edit_car(
            self,
            administrator_nickname,
            company_id,
            car_id,
            body_type=None,
            download_type=None,
            carrying_capacity=None,
            volume=None,
            loading_date_from=None,
            loading_date_by=None,
            country_loading=None,
            country_unloading=None,
            rate=None,
            price=None,
            form_price=None,
            note=None,
            urgently=None):
        administrator = self.get_user(nickname=administrator_nickname)


        if administrator.role.value > 1 and administrator.company_id == company_id:
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
                car.country_loading = country_loading

            if country_unloading is not None:
                car.country_unloading = country_unloading

            if rate is not None:
                car.rate = rate

            if price is not None:
                car.price = price

            if form_price is not None:
                car.form_price = form_price

            if note is not None:
                car.note = note

            if urgently is not None:
                car.urgently = urgently

            self._session.commit()

    def delete_car(self, administrator_nickname, company_id, car_id):
        administrator = self.get_user(nickname=administrator_nickname)
        company = self.get_company(company_id)
        car = self.get_car(car_id)

        if administrator.role.value > 1 and administrator.nickname == company.nickname:
            requests = self.get_requests(car_id=car.id)

            for request in requests:
                if request.status.value == 1:
                    request.status = Status(3)

            self._delete(car)

            text_log = REMOVE_CAR
            self.create_log(administrator.company_id, administrator.nickname, text_log)


    def create_user(
            self,
            nickname,
            name,
            surname,
            email,
            phone,
            avatar_path="../sources/default.txt"):

        user = User(
            nickname,
            name,
            surname,
            email,
            phone,
            None,
            Role(1),
            avatar_path
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

    def get_users(self, company_id=None, role=None):
        _filter = and_(
            or_(company_id is None, User.company_id == company_id),
            or_(role is None, User.role == role)
        )

        users = self._session.query(User).filter(_filter).all()
        self._session.commit()

        return users

    def is_administrator(self, user_id, company_id):
        user = self.get_user(user_id)

        return True if (user.company_id == int(company_id) and user.role == Role(2)) or user.role == Role(3) or user.role == Role(4) else False

    def is_employee(self, user_id, company_id):
        user = self.get_user(user_id=user_id)

        return True if user.company_id == int(company_id) or self.is_admin(user) or self.is_moder(user) else False

    def edit_user(
            self,
            nickname,
            name=None,
            surname=None,
            email=None,
            phone=None,
            avatar=None):
        user = self.get_user(nickname=nickname)

        if name is not None:
            user.name = name

        if surname is not None:
            user.surname = surname

        if email is not None:
            user.email = email

        if phone is not None:
            user.phone = phone

        if avatar is not None:
            user.avatar = avatar

        self._session.commit()

    def add_user_to_company(self, administrator, nickname, company_id):
        user = self.get_user(nickname=nickname)

        if not user:
            return False, False
        if user.company_id:
            return True, False
        else:
            user.add_company(company_id)

            text_log = ADD_EMPLOYEE % user.nickname
            self.create_log(company_id, administrator, text_log)

            self._add(user)

            return True, True

    def remove_user_from_company(self, administrator_nickname, _, user_id):
        user = self.get_user(user_id=user_id)
        administrator = self.get_user(nickname=administrator_nickname)

        if administrator.role.value > 1 and administrator.company_id == user.company_id and administrator_nickname != user.nickname:
            user.remove_company()

            text_log = REMOVE_EMPLOYEE % user.nickname
            self.create_log(administrator.company_id, administrator.nickname, text_log)

            self._add(user)

    def administrator(self, administrator_nickname, user_id):
        administrator = self.get_user(nickname=administrator_nickname)
        user = self.get_user(user_id=user_id)

        if administrator.role.value > 1 and administrator.company_id == user.company_id:
            if user.role == Role(1):
                user.role = Role(2)

                text_log = RAISING_TO_ADMINISTRATOR % user.nickname
                self.create_log(administrator.company_id, administrator.nickname, text_log)
            else:
                user.role = Role(1)

                text_log = LOWERING_FROM_ADMINISTRATOR % user.nickname
                self.create_log(administrator.company_id, administrator.nickname, text_log)
            self._add(user)

    def delete_user(self, user_id):
        user = self.get_user(user_id=user_id)

        self._delete(user)

    def create_goods(
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

        goods = Goods(
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
            note,
            urgently
        )

        self._add(goods)

        return goods.id

    def get_search_goods(
            self,
            body_type=None,
            download_type=None,
            weigh_min=None,
            weigh_max=None,
            volume_min=None,
            volume_max=None,
            loading_date_from=None,
            loading_date_by=None,
            country_loading=None,
            country_unloading=None,
            user_id=None):
        if body_type and int(body_type) == -1:
            body_type = None

        if download_type and int(download_type) == -1:
            download_type = None

        if not country_loading:
            country_loading = None

        if not country_unloading:
            country_unloading = None

        _filter = and_(
            or_(body_type is None, Goods.body_type == body_type),
            or_(download_type is None, Goods.download_type == download_type),
            or_(country_loading is None, Goods.country_loading == country_loading),
            or_(country_unloading is None, Goods.country_unloading == country_unloading),
            or_(user_id is None, Goods.user_id == user_id)
        )

        search_goods = self._session.query(Goods).filter(_filter).all()
        self._session.commit()

        result_goods = []

        for good in search_goods:
            if weigh_min:
                if good.weigh >= int(weigh_min):
                    result_goods.append(good)
            else:
                result_goods.append(good)

        search_goods = result_goods.copy()
        result_goods = []
        for good in search_goods:
            if weigh_max:
                if good.weigh <= int(weigh_max):
                    result_goods.append(good)
            else:
                result_goods.append(good)

        search_goods = result_goods.copy()
        result_goods = []
        for good in search_goods:
            if volume_min:
                if good.volume >= int(volume_min):
                    result_goods.append(good)
            else:
                result_goods.append(good)

        search_goods = result_goods.copy()
        result_goods = []
        for good in search_goods:
            if volume_max:
                if good.volume <= int(volume_max):
                    result_goods.append(good)
            else:
                result_goods.append(good)

        utc=pytz.UTC
        search_goods = result_goods.copy()
        result_goods = []
        for good in search_goods:
            if loading_date_from:
                if good.loading_date_from.replace(tzinfo=utc) >= loading_date_from:
                    result_goods.append(good)
            else:
                result_goods.append(good)

        search_goods = result_goods.copy()
        result_goods = []
        for good in search_goods:
            if loading_date_by:
                if good.loading_date_by.replace(tzinfo=utc) <= loading_date_by:
                    result_goods.append(good)
            else:
                result_goods.append(good)

        return result_goods

    def get_goods(self, goods_id):
        try:
            return (self._session.query(Goods)
                    .filter(Goods.id == goods_id).one_or_none())
        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Goods not found")

    def edit_goods(
            self,
            goods_id,
            name=None,
            body_type=None,
            download_type=None,
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

        if download_type is not None:
            goods.download_type = download_type

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

    def delete_goods(self, user_id, goods_id):
        goods = self.get_goods(goods_id)

        if goods.user_id == user_id:
            requests = self.get_requests(goods_id=goods.id)

            for request in requests:
                if request.status.value == 1:
                    request.status = Status(3)

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

        user = self.get_user(nickname=nickname)
        user.company_id = company.id
        user.role = Role(2)

        self._session.commit()

        return company.id

    def get_company(self, company_id=None, nickname=None):
        try:
            if nickname is not None:
                return (self._session.query(Company)
                    .filter(Company.nickname == nickname).one_or_none())
            else:
                return (self._session.query(Company)
                        .filter(Company.id == company_id).one_or_none())
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
            company_id,
            UNP=None,
            name=None,
            primary_occupation=None,
            license=None,
            country=None,
            town=None,
            address=None,
            phone=None,
            description=None):
        company = self.get_company(company_id=company_id)

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
            user_id,
            datetime.datetime.now() + datetime.timedelta(hours=3)
        )

        self._add(review)

        return review.id

    def edit_review(
            self,
            company_id,
            user_id,
            text):

        review = self.get_review(company_id, user_id)

        review.review = text
        review.is_edit = True

        self._session.commit()


    def get_reviews(self, company_id):
        try:
            return (self._session.query(Review)
                .filter(Review.company_id == company_id).all())

        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Review not found")


    def get_ratings(self, company_id):
        rating = []
        for i in range(1, 4):
            _filter = and_(
                or_(Review.company_id == company_id),
                or_(Review.rating == Rating(i))
            )
            rating.append(len(self._session.query(Review).filter(_filter).all()))

        return rating


    def get_review(self, company_id, user_id, review_id=None):
        _filter = and_(
            or_(Review.company_id == company_id),
            or_(Review.user_id == user_id),
            or_(review_id is None, Review.id == review_id)
        )
        review = self._session.query(Review).filter(_filter).one_or_none()

        return review

    def has_already_rated(self, company_id, user_id):
        review = self.get_review(company_id, user_id)

        return review is not None


    def change_rating(self, company_id, user_id, rating):
        review = self.get_review(company_id, user_id)

        if review.review is None:
            if review.rating != Rating(rating):
                review.rating = Rating(rating)
            else:
                self.delete_review(company_id, user_id)

            self._session.commit()


    def delete_review(self, company_id, user_id):
        review = self.get_review(company_id, user_id)

        self._delete(review)


    def get_company_rating(self, company_id):
        reviews = self.get_reviews(company_id)
        rating = [0, 0, 0]

        for review in reviews:
            rating[review.rating.value - 1] += 1

        return rating

    def create_log(
            self,
            company_id,
            username,
            text,
            link_text=None,
            link=None):

        log = Log(
            company_id,
            username,
            datetime.datetime.now() + datetime.timedelta(hours=3),
            text,
            link_text,
            link
        )

        self._add(log)

        return log.id

    def get_logs(
            self,
            company_id):
        try:
            return (self._session.query(Log)
                    .filter(Log.company_id == company_id).all())
        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Log not found")


    def create_message(
            self,
            sender_id,
            recipient_id,
            text):

        message = Message(
            sender_id,
            recipient_id,
            text
        )

        self._add(message)

        return message.id


    def get_messages(self, sender_id, recipient_id=None, distinct=False):
        _filter = or_(
            and_(
                or_(Message.sender_id == sender_id),
                or_(recipient_id is None, Message.recipient_id == recipient_id)
            ),
            and_(
                or_(recipient_id is None, Message.sender_id == recipient_id),
                or_(Message.recipient_id == sender_id)
            )
        )

        if distinct:
            temp_messages = self._session.query(Message).filter(_filter).distinct(Message.recipient_id).group_by(Message.sender_id, Message.recipient_id).all()
            self._session.commit()
            messages = self._remove_repeat_messages(temp_messages)
        else:
            messages = self._session.query(Message).filter(_filter).all()
            self._session.commit()

        return messages


    def _remove_repeat_messages(self, messages):
        delete_list = set()
        for i in reversed(range(len(messages))):
            for j in reversed(range(len(messages))):
                if messages[i].sender_id == messages[j].recipient_id and messages[i].recipient_id == messages[j].sender_id and i != j:
                    if messages[i].id > messages[j].id:
                        delete_list.add(j)
                        break
                    else:
                        delete_list.add(i)
                        break

        delete_list = sorted(delete_list, reverse=True)
        for i in delete_list:
            del messages[i]

        messages = sorted(messages, key=lambda message: message.id, reverse=True)
        return messages


    def create_request(
            self,
            user_id,
            car_id=None,
            goods_id=None):

        if (car_id and not self.get_requests(user_id, car_id=car_id)) or (goods_id and not self.get_requests(user_id, goods_id=goods_id)):
            request = Request(
                user_id,
                car_id,
                goods_id,
                datetime.datetime.now() + datetime.timedelta(hours=3)
            )

            self._add(request)

            return request.id


    def get_request(self, request_id=None, user_id=None, car_id=None, goods_id=None):
        _filter = and_(
            or_(request_id is None, Request.id == request_id),
            or_(user_id is None, Request.user_id == user_id),
            or_(car_id is None, Request.car_id == car_id),
            or_(goods_id is None, Request.goods_id == goods_id)
        )
        try:
            return (self._session.query(Request)
                    .filter(_filter).one_or_none())
        except sqlalchemy.orm.exc.NoResultFound:
            raise Exception("Request not found")


    def get_requests(self, user_id=None, car_id=None, goods_id=None):
        _filter = and_(
            or_(user_id is None, Request.user_id == user_id),
            or_(car_id is None, Request.car_id == car_id),
            or_(goods_id is None, Request.goods_id == goods_id)
        )

        request = self._session.query(Request).filter(_filter).all()
        self._session.commit()

        return request


    def accept_request(self, company_id, administrator_nickname, car_id, request_id, log=True):
        request = self.get_request(request_id=request_id)

        request.status = Status(2)
        request.date = datetime.datetime.now() + datetime.timedelta(hours=3)

        if log:
            text_log = ACCEPT_REQUEST
            self.create_log(company_id, administrator_nickname, text_log, "машины", car_id)

        self._session.commit()


    def reject_request(self, company_id, administrator_nickname, car_id, request_id, log=True):
        request = self.get_request(request_id=request_id)

        request.status = Status(3)
        request.date = datetime.datetime.now() + datetime.timedelta(hours=3)

        if log:
            text_log = REJECT_REQUEST
            self.create_log(company_id, administrator_nickname, text_log, "машины", car_id)

        self._session.commit()


    def delete_request(self, request_id):
        request = self.get_request(request_id)

        self._delete(request)


    def is_admin(self, user):
        return True if user.role == Role(4) else False

    def is_moder(self, user):
        return True if user.role == Role(3) else False


    def change_permission(self, admin, user_id, role):
        if admin.role == Role(4):
            user = self.get_user(user_id)

            if role == 1:
                company = self.get_company(nickname=user.nickname)

                user.role = Role(2) if company else Role(1)
            else:
                user.role = Role(role)

            self._session.commit()


    def _add(self, object):
        self._session.add(object)
        self._session.commit()

    def _delete(self, object):
        self._session.delete(object)
        self._session.commit()
