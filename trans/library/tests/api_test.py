import os
import unittest
import time
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta

from library.api.api import API
from library.models.user import User, Role
from library.models.review import Rating
from library.models.request import Status

utc=pytz.UTC

TEST_USER_NICKNAME = "test_user_nickname"
TEST_USER_NAME = "test_user_name"
TEST_USER_SURNAME = "test_user_surname"
TEST_USER_EMAIL = "test@yandex.ru"
TEST_COMPANY_UNP = "158125239"
TEST_COMPANY_NAME = "test_company_name"
TEST_COMPANY_PRIMARY_OCCUPATION = "Грузовладелец"
TEST_COMPANY_LICENSE = "02180/6-24641"
TEST_COMPANY_TOWN = "test_company_town"
TEST_COMPANY_ADDRESS = "test_company_address"
TEST_PHONE = "+375332834172"
TEST_COUNTRY = "test_country"
TEST_DESCRIPTION = "test_description"
TEST_GOODS_NAME = "test_goods"
TEST_BODY_TYPE = "1"
TEST_DOWNLOAD_TYPE = "1"
TEST_CAR_COUNT = 1
TEST_BELT_COUNT = 1
TEST_GOODS_WEIGH = 2
TEST_VOLUME = 3
TEST_LOADING_DATE_FROM = datetime(2000, 1, 1).replace(tzinfo=utc)
TEST_LOADING_DATE_BY = datetime(2001, 1, 1).replace(tzinfo=utc)
TEST_COUNTRY_LOADING = "test_country_loading"
TEST_COUNTRY_UNLOADING = "test_country_unloading"
TEST_RATE = 4
TEST_PRICE = "USD"
TEST_FORM_PRICE = "test_form_price"
TEST_NOTE = "test_note"
TEST_CAR_CARRYING_CAPACITY = 6
TEST_REVIEW_RATING = 1
TEST_REVIEW = "test_review"


DATABASE_NAME = "database_test"
CONNECTION_STRING = "sqlite:///" + DATABASE_NAME

class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = API(CONNECTION_STRING)

    def tearDown(self):
        os.remove(DATABASE_NAME)

    def create_user(self, nickname=TEST_USER_NICKNAME):
        user_id = self.api.create_user(
            nickname,
            TEST_USER_NAME,
            TEST_USER_SURNAME,
            TEST_USER_EMAIL,
            TEST_PHONE,
            avatar_path="sources/default.txt"
        )
        return user_id

    def create_company(self):
        self.create_user()

        company_id = self.api.create_company(
            TEST_USER_NICKNAME,
            TEST_COMPANY_UNP,
            TEST_COMPANY_NAME,
            TEST_COMPANY_PRIMARY_OCCUPATION,
            TEST_COMPANY_LICENSE,
            TEST_COUNTRY,
            TEST_COMPANY_TOWN,
            TEST_COMPANY_ADDRESS,
            TEST_PHONE,
            TEST_DESCRIPTION
        )
        return company_id

    def create_goods(self, user_id):
        goods_id = self.api.create_goods(
            user_id,
            TEST_GOODS_NAME,
            TEST_BODY_TYPE,
            TEST_CAR_COUNT,
            TEST_DOWNLOAD_TYPE,
            TEST_BELT_COUNT,
            TEST_GOODS_WEIGH,
            TEST_VOLUME,
            TEST_LOADING_DATE_FROM,
            TEST_LOADING_DATE_BY,
            TEST_COUNTRY_LOADING,
            TEST_COUNTRY_UNLOADING,
            TEST_RATE,
            TEST_PRICE,
            TEST_FORM_PRICE,
            TEST_NOTE
        )

        return goods_id

    def create_car(self, nickname, company_id):
        car_id = self.api.create_car(
            nickname,
            company_id,
            TEST_BODY_TYPE,
            TEST_DOWNLOAD_TYPE,
            TEST_CAR_CARRYING_CAPACITY,
            TEST_VOLUME,
            TEST_LOADING_DATE_FROM,
            TEST_LOADING_DATE_BY,
            TEST_COUNTRY_LOADING,
            TEST_COUNTRY_UNLOADING,
            TEST_RATE,
            TEST_PRICE,
            TEST_FORM_PRICE,
            TEST_NOTE
        )

        return car_id

    def create_reviwe(self, user_id, company_id):
        review_id = self.api.create_review(
            TEST_REVIEW_RATING,
            TEST_REVIEW,
            company_id,
            user_id
        )

        return review_id

    def edit_car(self, nickname, company_id, car_id):
        self.api.edit_car(
            nickname,
            company_id,
            car_id,
            body_type="3",
            download_type="4",
            carrying_capacity=5,
            volume=6,
            loading_date_from=datetime(2002, 1, 1).replace(tzinfo=utc),
            loading_date_by=datetime(2003, 1, 1).replace(tzinfo=utc),
            country_loading="country_loading",
            country_unloading="country_unloading",
            rate=10,
            price="price",
            form_price="form_price",
            note="note"
        )

    def create_message(self, sender_id, recipient_id, text):
        message_id = self.api.create_message(
            sender_id,
            recipient_id,
            text
        )

        return message_id

    def create_request(self, user_id, car_id=None, goods_id=None):
        request_id = self.api.create_request(
            user_id,
            car_id,
            goods_id
        )

        return request_id

    def test_create_user(self):
        user_id = self.create_user()

        user_count = len(self.api.get_users())
        self.assertEqual(user_count, 1)

        test_user = [
            self.api.get_user(user_id=user_id),
            self.api.get_user(nickname=TEST_USER_NICKNAME)
        ]

        for user in test_user:
            self.assertIsInstance(user, User)

            self.assertEqual(user.nickname, TEST_USER_NICKNAME)
            self.assertEqual(user.name, TEST_USER_NAME)
            self.assertEqual(user.surname, TEST_USER_SURNAME)
            self.assertEqual(user.email, TEST_USER_EMAIL)
            self.assertEqual(user.phone, TEST_PHONE)
            self.assertEqual(user.company_id, None)
            self.assertEqual(user.role, Role(1))

    def test_edit_user(self):
        user_id = self.create_user()
        user = self.api.get_user(user_id=user_id)

        self.assertEqual(user.nickname, TEST_USER_NICKNAME)

        self.api.edit_user(
            TEST_USER_NICKNAME,
            name="test",
            surname="test",
            email="test_email@yandex.ru",
            phone="+375292123214"
        )

        self.assertEqual(user.nickname, TEST_USER_NICKNAME)
        self.assertEqual(user.name, "test")
        self.assertEqual(user.surname, "test")
        self.assertEqual(user.email, "test_email@yandex.ru")
        self.assertEqual(user.phone, "+375292123214")
        self.assertEqual(user.company_id, None)
        self.assertEqual(user.role, Role(1))

    def test_delete_user(self):
        user_id = self.create_user()

        user_count = len(self.api.get_users())
        self.assertEqual(user_count, 1)

        self.api.delete_user(user_id)

        user_count = len(self.api.get_users())
        self.assertEqual(user_count, 0)

    def test_create_company(self):
        company_id = self.create_company()

        user_count = len(self.api.get_users())
        self.assertEqual(user_count, 1)

        user = self.api.get_user(user_id=1)

        company_count = len(self.api.get_companys())
        self.assertEqual(company_count, 1)

        test_company = [
            self.api.get_company(company_id=company_id),
            self.api.get_company(nickname=TEST_USER_NICKNAME)
        ]

        for company in test_company:
            self.assertEqual(company.nickname, TEST_USER_NICKNAME)
            self.assertEqual(company.UNP, TEST_COMPANY_UNP)
            self.assertEqual(company.name, TEST_COMPANY_NAME)
            self.assertEqual(company.primary_occupation, TEST_COMPANY_PRIMARY_OCCUPATION)
            self.assertEqual(company.license, TEST_COMPANY_LICENSE)
            self.assertEqual(company.country, TEST_COUNTRY)
            self.assertEqual(company.town, TEST_COMPANY_TOWN)
            self.assertEqual(company.address, TEST_COMPANY_ADDRESS)
            self.assertEqual(company.phone, TEST_PHONE)
            self.assertEqual(company.description, TEST_DESCRIPTION)

            self.assertEqual(user.company_id, company_id)


    def test_edit_company(self):
        company_id = self.create_company()

        self.api.edit_company(
            TEST_USER_NICKNAME,
            UNP="unp",
            name="name",
            primary_occupation="primary_occupation",
            license="license",
            country="country",
            town="town",
            address="address",
            phone="phone",
            description="description"
        )

        company = self.api.get_company(company_id=company_id)

        self.assertEqual(company.nickname, TEST_USER_NICKNAME)
        self.assertEqual(company.UNP, "unp")
        self.assertEqual(company.name, "name")
        self.assertEqual(company.primary_occupation, "primary_occupation")
        self.assertEqual(company.license, "license")
        self.assertEqual(company.country, "country")
        self.assertEqual(company.town, "town")
        self.assertEqual(company.address, "address")
        self.assertEqual(company.phone, "phone")
        self.assertEqual(company.description, "description")

    def test_delete_company(self):
        company_id = self.create_company()

        self.api.delete_company(company_id=company_id)

        user_count = len(self.api.get_users())
        self.assertEqual(user_count, 1)

        company_count = len(self.api.get_companys())
        self.assertEqual(company_count, 0)

    def test_add_user_to_company(self):
        company_id = self.create_company()
        user_id = self.create_user(nickname="test_user")

        administrator = self.api.get_user(user_id=1)
        user = self.api.get_user(user_id=user_id)

        self.assertEqual(administrator.id, 1)
        self.assertEqual(user.id, 2)

        self.api.add_user_to_company(administrator.nickname, user.nickname, company_id)

        self.assertEqual(user.nickname, "test_user")

        user_count = len(self.api.get_users(company_id=company_id))

        self.assertEqual(user.company_id, company_id)
        self.assertEqual(administrator.company_id, company_id)
        self.assertEqual(user_count, 2)
        self.assertEqual(administrator.role, Role(2))
        self.assertEqual(user.role, Role(1))

        log = len(self.api.get_logs(company_id))
        self.assertEqual(log, 1)

    def test_administrator(self):
        company_id = self.create_company()
        user_id = self.create_user(nickname="test_user")

        administrator = self.api.get_user(user_id=1)
        user = self.api.get_user(user_id=user_id)

        self.api.add_user_to_company(administrator.nickname, user.nickname, company_id)
        self.assertEqual(user.role, Role(1))

        self.api.administrator(administrator.nickname, user_id)
        self.assertEqual(user.role, Role(2))
        self.assertEqual(user.company_id, company_id)

    def test_remove_user_from_company(self):
        company_id = self.create_company()
        user_id = self.create_user(nickname="test_user")

        administrator = self.api.get_user(user_id=1)
        user = self.api.get_user(user_id=user_id)

        self.api.add_user_to_company(administrator.nickname, user.nickname, company_id)

        self.assertEqual(user.role, Role(1))
        self.api.administrator(user.nickname, user_id)
        self.assertEqual(user.role, Role(1))

        self.api.administrator(administrator.nickname, user_id)
        self.assertEqual(user.role, Role(2))

        self.api.remove_user_from_company(administrator.nickname, user_id, user_id)

        user_count = len(self.api.get_users(company_id=company_id))

        self.assertNotEqual(user.company_id, company_id)
        self.assertEqual(administrator.company_id, company_id)
        self.assertEqual(user_count, 1)
        self.assertEqual(administrator.role, Role(2))
        self.assertEqual(user.role, Role(1))

        log = len(self.api.get_logs(company_id))
        self.assertEqual(log, 3)

    def test_create_goods(self):
        user_id = self.create_user()
        goods_id = self.create_goods(user_id)

        goods = self.api.get_goods(goods_id)
        user = self.api.get_user(user_id)

        self.assertEqual(goods.name, TEST_GOODS_NAME)
        self.assertEqual(goods.body_type, TEST_BODY_TYPE)
        self.assertEqual(goods.car_count, TEST_CAR_COUNT)
        self.assertEqual(goods.download_type, TEST_DOWNLOAD_TYPE)
        self.assertEqual(goods.belt_count, TEST_BELT_COUNT)
        self.assertEqual(goods.weigh, TEST_GOODS_WEIGH)
        self.assertEqual(goods.volume, TEST_VOLUME)
        self.assertEqual(goods.loading_date_from.replace(tzinfo=utc), TEST_LOADING_DATE_FROM)
        self.assertEqual(goods.loading_date_by.replace(tzinfo=utc), TEST_LOADING_DATE_BY)
        self.assertEqual(goods.country_loading, TEST_COUNTRY_LOADING)
        self.assertEqual(goods.country_unloading, TEST_COUNTRY_UNLOADING)
        self.assertEqual(goods.rate, TEST_RATE)
        self.assertEqual(goods.price, TEST_PRICE)
        self.assertEqual(goods.form_price, TEST_FORM_PRICE)
        self.assertEqual(goods.note, TEST_NOTE)

        search_goods = self.api.get_search_goods(
            TEST_BODY_TYPE,
            TEST_DOWNLOAD_TYPE,
            TEST_GOODS_WEIGH,
            TEST_GOODS_WEIGH,
            TEST_VOLUME,
            TEST_VOLUME,
            TEST_LOADING_DATE_FROM,
            TEST_LOADING_DATE_BY,
            TEST_COUNTRY_LOADING,
            TEST_COUNTRY_UNLOADING,
            user.id
        )

        self.assertEqual(len(search_goods), 1)

    def test_create_car(self):
        company_id = self.create_company()
        user = self.api.get_user(nickname=TEST_USER_NICKNAME)

        car_id = self.create_car(user.nickname, company_id)
        car = self.api.get_car(car_id)

        self.assertEqual(car.company_id, company_id)
        self.assertEqual(car.body_type, TEST_BODY_TYPE)
        self.assertEqual(car.download_type, TEST_DOWNLOAD_TYPE)
        self.assertEqual(car.carrying_capacity, TEST_CAR_CARRYING_CAPACITY)
        self.assertEqual(car.volume, TEST_VOLUME)
        self.assertEqual(car.loading_date_from.replace(tzinfo=utc), TEST_LOADING_DATE_FROM)
        self.assertEqual(car.loading_date_by.replace(tzinfo=utc), TEST_LOADING_DATE_BY)
        self.assertEqual(car.country_loading, TEST_COUNTRY_LOADING)
        self.assertEqual(car.country_unloading, TEST_COUNTRY_UNLOADING)
        self.assertEqual(car.rate, TEST_RATE)
        self.assertEqual(car.price, TEST_PRICE)
        self.assertEqual(car.form_price, TEST_FORM_PRICE)
        self.assertEqual(car.note, TEST_NOTE)

        logs = self.api.get_logs(company_id)

        self.assertEqual(len(logs), 1)

    def test_get_cars(self):
        company_id = self.create_company()
        user = self.api.get_user(nickname=TEST_USER_NICKNAME)

        self.create_car(user.nickname, company_id)
        car = self.api.get_cars(
            TEST_BODY_TYPE,
            TEST_DOWNLOAD_TYPE,
            TEST_CAR_CARRYING_CAPACITY,
            TEST_CAR_CARRYING_CAPACITY,
            TEST_VOLUME,
            TEST_VOLUME,
            TEST_LOADING_DATE_FROM,
            TEST_LOADING_DATE_BY,
            TEST_COUNTRY_LOADING,
            TEST_COUNTRY_UNLOADING,
            company_id
        )

        self.assertEqual(len(car), 1)

    def test_edit_car(self):
        company_id = self.create_company()
        administrator = self.api.get_user(nickname=TEST_USER_NICKNAME)

        car_id = self.create_car(administrator.nickname, company_id)
        user_id = self.create_user("user")
        user = self.api.get_user(user_id=user_id)

        self.edit_car(user.nickname, company_id, car_id)

        car = self.api.get_car(car_id)

        self.assertEqual(car.company_id, company_id)
        self.assertEqual(car.body_type, TEST_BODY_TYPE)
        self.assertEqual(car.download_type, TEST_DOWNLOAD_TYPE)
        self.assertEqual(car.carrying_capacity, TEST_CAR_CARRYING_CAPACITY)
        self.assertEqual(car.volume, TEST_VOLUME)
        self.assertEqual(car.loading_date_from.replace(tzinfo=utc), TEST_LOADING_DATE_FROM)
        self.assertEqual(car.loading_date_by.replace(tzinfo=utc), TEST_LOADING_DATE_BY)
        self.assertEqual(car.country_loading, TEST_COUNTRY_LOADING)
        self.assertEqual(car.country_unloading, TEST_COUNTRY_UNLOADING)
        self.assertEqual(car.rate, TEST_RATE)
        self.assertEqual(car.price, TEST_PRICE)
        self.assertEqual(car.form_price, TEST_FORM_PRICE)
        self.assertEqual(car.note, TEST_NOTE)

        self.edit_car(administrator.nickname, company_id, car_id)

        car = self.api.get_car(car_id)

        self.assertEqual(car.company_id, company_id)
        self.assertEqual(car.body_type, "3")
        self.assertEqual(car.download_type, "4")
        self.assertEqual(car.carrying_capacity, 5)
        self.assertEqual(car.volume, 6)
        self.assertEqual(car.loading_date_from.replace(tzinfo=utc), datetime(2002, 1, 1).replace(tzinfo=utc))
        self.assertEqual(car.loading_date_by.replace(tzinfo=utc), datetime(2003, 1, 1).replace(tzinfo=utc))
        self.assertEqual(car.country_loading, "country_loading")
        self.assertEqual(car.country_unloading, "country_unloading")
        self.assertEqual(car.rate, 10)
        self.assertEqual(car.price, "price")
        self.assertEqual(car.form_price, "form_price")
        self.assertEqual(car.note, "note")

        logs = self.api.get_logs(company_id)
        self.assertEqual(len(logs), 1)

    def test_create_review(self):
        company_id = self.create_company()

        user_id = self.create_user("user")

        self.create_reviwe(user_id, company_id)
        test_review = [
            self.api.get_review(company_id, user_id),
            self.api.get_reviews(company_id)[0]
        ]

        for review in test_review:
            self.assertEqual(review.rating, Rating(1))
            self.assertEqual(review.review, TEST_REVIEW)

        if not self.api.has_already_rated(company_id, user_id):
            self.create_reviwe(user_id, company_id)

        review_count = len(self.api.get_reviews(company_id))

        self.assertEqual(review_count, 1)

    def test_message(self):
        sender_id = self.create_user(nickname="sender")
        recipient_1_id = self.create_user(nickname="recipient_1")
        recipient_2_id = self.create_user(nickname="recipient_2")

        self.create_message(sender_id, recipient_1_id, "text_1")
        self.create_message(recipient_1_id, sender_id, "text_2")
        self.create_message(sender_id, recipient_2_id, "text_3")
        self.create_message(recipient_2_id, sender_id, "text_4")

        messages_count = len(self.api.get_messages(sender_id))
        self.assertEqual(messages_count, 4)

        messages_count = len(self.api.get_messages(sender_id, distinct=True))
        self.assertEqual(messages_count, 2)

        messages_count = len(self.api.get_messages(recipient_1_id, distinct=True))
        self.assertEqual(messages_count, 1)

        messages_count = len(self.api.get_messages(recipient_2_id, distinct=True))
        self.assertEqual(messages_count, 1)

        messages_count = len(self.api.get_messages(sender_id, recipient_1_id))
        self.assertEqual(messages_count, 2)

        messages_count = len(self.api.get_messages(sender_id, recipient_2_id))
        self.assertEqual(messages_count, 2)

        messages_count = len(self.api.get_messages(recipient_1_id, sender_id))
        self.assertEqual(messages_count, 2)

        messages_count = len(self.api.get_messages(recipient_2_id, sender_id))
        self.assertEqual(messages_count, 2)

        messages = self.api.get_messages(sender_id)
        for i in range(len(messages)):
            self.assertEqual(messages[i].text, "text_" + str(i + 1))

    def test_create_request(self):
        company_id = self.create_company()
        administrator = self.api.get_user(nickname=TEST_USER_NICKNAME)

        car_id = self.create_car(administrator.nickname, company_id)
        goods_id = self.create_goods(administrator.id)

        user_id = self.create_user(nickname="user")

        request_car_id = self.create_request(user_id, car_id=car_id)
        request_goods_id = self.create_request(user_id, goods_id=goods_id)

        requests = self.api.get_requests(user_id)
        self.assertEqual(len(requests), 2)

        request_car = self.api.get_request(request_car_id)
        request_goods = self.api.get_request(request_goods_id)

        self.assertTrue(request_car)
        self.assertTrue(request_goods)
        self.assertEqual(request_car.status, Status(1))
        self.assertEqual(request_goods.status, Status(1))

    def test_accept_request(self):
        company_id = self.create_company()
        administrator = self.api.get_user(nickname=TEST_USER_NICKNAME)

        car_id = self.create_car(administrator.nickname, company_id)
        goods_id = self.create_goods(administrator.id)

        user_id = self.create_user(nickname="user")

        request_car_id = self.create_request(user_id, car_id=car_id)
        request_goods_id = self.create_request(user_id, goods_id=goods_id)

        self.api.accept_request(company_id, administrator.nickname, car_id, request_car_id)
        self.api.accept_request(company_id, administrator.nickname, goods_id, request_goods_id)

        request_car = self.api.get_request(request_car_id)
        request_goods = self.api.get_request(request_goods_id)

        self.assertTrue(request_car)
        self.assertTrue(request_goods)
        self.assertEqual(request_car.status, Status(2))
        self.assertEqual(request_goods.status, Status(2))

    def test_reject_request(self):
        company_id = self.create_company()
        administrator = self.api.get_user(nickname=TEST_USER_NICKNAME)

        car_id = self.create_car(administrator.nickname, company_id)
        goods_id = self.create_goods(administrator.id)

        user_id = self.create_user(nickname="user")

        request_car_id = self.create_request(user_id, car_id=car_id)
        request_goods_id = self.create_request(user_id, goods_id=goods_id)

        self.api.reject_request(company_id, administrator.nickname, car_id, request_car_id)
        self.api.reject_request(company_id, administrator.nickname, goods_id, request_goods_id)

        request_car = self.api.get_request(request_car_id)
        request_goods = self.api.get_request(request_goods_id)

        self.assertTrue(request_car)
        self.assertTrue(request_goods)
        self.assertEqual(request_car.status, Status(3))
        self.assertEqual(request_goods.status, Status(3))

    def test_delete_car(self):
        company_id = self.create_company()
        administrator = self.api.get_user(nickname=TEST_USER_NICKNAME)

        car_id = self.create_car(administrator.nickname, company_id)
        user_id = self.create_user(nickname="user")

        self.create_request(user_id, car_id=car_id)

        self.api.delete_car(administrator.nickname, company_id, car_id)

        cars = self.api.get_cars(company_id=company_id)
        self.assertEqual(len(cars), 0)

        requests = self.api.get_request(car_id=car_id)
        self.assertEqual(requests.status, Status(3))

    def test_delete_goods(self):
        administrator = self.api.get_user(user_id=self.create_user())

        goods_id = self.create_goods(administrator.id)
        user_id = self.create_user(nickname="user")

        self.create_request(user_id, goods_id=goods_id)

        self.api.delete_goods(administrator.id, goods_id)

        goods = self.api.get_goods(goods_id)
        self.assertIsNone(goods)

        requests = self.api.get_request(goods_id=goods_id)
        self.assertEqual(requests.status, Status(3))


if __name__ == "__main__":
    unittest.main()
