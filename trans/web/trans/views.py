from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm
)
from django.http import HttpResponse

from django.shortcuts import (
    render,
    redirect
)

from . import get_api
from .forms import (
    UserForm,
    EditUserForm,
    CompanyForm,
    ReviewForm,
    EmployeeForm,
    CarForm,
    GoodsForm
)
from library.models.user import Role

from datetime import datetime
import pytz
import math
import requests
import base64

PRIMARY_OCCUPATION = [
    "Перевозчик",
    "Грузовладелец",
    "Экспедитор",
    "Логистические центры и склады",
    "Таможенные услуги",
    "Дилеры, автохаусы, перегон",
    "Запчасти, Шины, АКБ",
    "Масла, Тех жидкости, Автохимия",
    "GPS, Тахографы, оборудование",
    "АЗС, Придорожный сервис",
    "СТО, Мойки, Шиномонтаж",
    "Банки, Страхование, Лизинг",
    "Эвакуаторы",
    "Спецтехника",
    "Автовозы",
    "Консалтинг, бухгалтерские услуги",
    "Другие",
]

BODY_TYPE_COVERED = [
    "Тент",
    "Рефрижератор",
    "Рефрижератор-тушевоз",
    "Изотерма",
    "Цельнометаллический",
    "Контейнер",
    "Микроавтобус",
]

BODY_TYPE_UNCOVERED = [
    "Бортовой",
    "Гидроманипулятор",
    "Металловоз (Ломовоз)",
    "Контейнеровоз",
    "Площадка без бортов",
    "Плитовоз",
    "Самосвал",
    "Трал (Негабарит)"
]

BODY_TYPE_TANK = [
    "Автоцистерна",
    "Битумовоз",
    "Бензовоз",
    "Бетоновоз",
    "Газовоз",
    "Кормовоз",
    "Молоковоз",
    "Муковоз",
    "Цементовоз"
]

BODY_TYPE_SPECIAL = [
    "Автовоз",
    "Зерновоз",
    "Катушковоз",
    "Коневоз",
    "Кран",
    "Лесовоз",
    "Мусоровоз",
    "Одеждовоз",
    "Птицевоз",
    "Рулоновоз",
    "Скотовоз",
    "Стекловоз",
    "Трубовоз",
    "Тягач",
    "Щеповоз",
    "Эвакуатор",
    "Другое"
]

BODY_TYPE = BODY_TYPE_COVERED.copy()
BODY_TYPE.extend(BODY_TYPE_UNCOVERED)
BODY_TYPE.extend(BODY_TYPE_TANK)
BODY_TYPE.extend(BODY_TYPE_SPECIAL)

DOWNLOAD_TYPE = [
    "Задняя",
    "Боковая",
    "Верхняя",
    "Со снятием стоек",
    "Со снятием поперечных перекладин",
    "Без ворот"
]

PRICES = [
    "Бел. руб.",
    "Бел. руб. / км",
    "Бел. руб. / час",
    "Рос. руб.",
    "Рос. руб. / км",
    "Рос. руб. / час",
    "USD",
    "USD / км",
    "USD / час",
    "EUR",
    "EUR / км",
    "EUR / час"
]

FORM_PRICES = [
    "Любая ф/о",
    "Безнал.",
    "Безнал. с НДС",
    "Безнал. без НДС",
    "Перевод по загрузке",
    "Перевод по выгрузке",
    "Предоплата"
]


def is_add_car(user):
    api = get_api()

    _company = None
    if user:
        _company = api.get_company(company_id=user.company_id) if api.is_administrator(user.id, user.company_id) else None

    return _company


def home(request):
    api = get_api()
    all_companys = api.get_companys()
    companys = []

    user = api.get_user(nickname=request.user.username)

    for company in all_companys:
        rating = api.get_ratings(company.id)
        review = api.get_review(company.id, user.id) if user else None

        companys.append((company, rating[0], rating[1], rating[2], True if review else False))

    return render(request, 'trans/home.html', {'fields': PRIMARY_OCCUPATION, 'companys': companys, 'my_company': is_add_car(user)})


def signup(request):
    api = get_api()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            api.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['name'],
                form.cleaned_data['surname'],
                form.cleaned_data['email'],
                form.cleaned_data['phone']
            )
            return redirect('/')
    else:
        form = UserForm()

    return render(request, 'registration/signup.html', {'form': form})


def profile(request, nickname):
    api = get_api()
    owner = api.get_user(nickname=request.user.username)

    user = api.get_user(nickname=nickname)
    company = api.get_company(company_id=user.company_id)
    is_administrator = False
    if company:
        is_administrator = api.is_administrator(owner.id, company.id)

    check = nickname == request.user.username
    show = not check or company != None

    return render(request, 'trans/profile.html', {'member': user, 'company': company, 'check': check, 'show': show, 'is_administrator': is_administrator, 'my_company': is_add_car(user)})


def add_company(request):
    api = get_api()
    user = request.user.username

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            api.create_company(
                user,
                form.cleaned_data['UNP'],
                form.cleaned_data['name'],
                PRIMARY_OCCUPATION[int(form.cleaned_data['primary_occupation'])],
                form.cleaned_data['license'],
                form.cleaned_data['country'],
                form.cleaned_data['town'],
                form.cleaned_data['address'],
                form.cleaned_data['phone'],
                form.cleaned_data['description']
            )
            return redirect('/profile/')
    else:
        form = CompanyForm()

    return render(request, 'trans/add_company.html', {'form': form, 'fields': PRIMARY_OCCUPATION, 'my_company': is_add_car(api.get_user(nickname=user))})


def edit_profile(request):
    api = get_api()
    user = request.user.username
    member = api.get_user(nickname=user)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = request.FILES['avatar'].file.getvalue() if request.FILES else None
            api.edit_user(
                user,
                form.cleaned_data['name'],
                form.cleaned_data['surname'],
                form.cleaned_data['email'],
                form.cleaned_data['phone'],
                avatar,
            )
            return redirect('/profile/' + user)

    return render(request, 'trans/edit_profile.html', {'form': member, 'my_company': is_add_car(api.get_user(nickname=user))})


def edit_company(request):
    api = get_api()
    user = request.user.username
    company = ""

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            api.edit_company(
                nickname=user,
                phone=form.cleaned_data['phone'],
                description=form.cleaned_data['description']
            )
            return redirect('/profile/' + user)

    else:
        company = api.get_company(nickname=user)
        number = PRIMARY_OCCUPATION.index(company.primary_occupation)

    return render(request, 'trans/edit_company.html', {'form': company, 'fields': PRIMARY_OCCUPATION, 'number': number, 'my_company': is_add_car(api.get_user(nickname=user))})


def edit_password(request):
    api = get_api()

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/profile/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'trans/change_password.html', {'form': form, 'my_company': is_add_car(api.get_user(nickname=request.user.username))})


def add_review(request, company_id):
    api = get_api()
    user_id = api.get_user(nickname=request.user.username).id

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            api.create_review(
                form.cleaned_data['rating'],
                form.cleaned_data['review'],
                company_id,
                user_id
            )
            return redirect('/')
    else:
        form = CompanyForm()

    company = api.get_company(company_id).name

    return render(request, 'trans/add_review.html', {'form': form, 'company': company, 'my_company': is_add_car(api.get_user(user_id=user_id))})


def get_review(request, company_id):
    api = get_api()

    company = api.get_company(company_id=company_id)
    company_reviews = api.get_reviews(company_id)
    negative, neutral, positive = api.get_company_rating(company_id)
    reviews = []

    for review in company_reviews:
        if review.review is not None:
            user = api.get_user(user_id=review.user_id)
            avatar = _get_avatar(user.avatar)

            reviews.append((review, user, review.date.strftime("%d.%m.%Y, %H:%M"), avatar))

    user = request.user.username

    return render(
        request, 'trans/review.html',
        {
            'reviews': reviews,
            'company': company,
            'negative': negative,
            'neutral': neutral,
            'positive': positive,
            'nickname': user,
            'my_company': is_add_car(api.get_user(nickname=user))
        })


def contacts(request, company_id):
    api = get_api()

    owner = request.user.username
    user = api.get_user(nickname=owner)

    company = api.get_company(company_id=company_id)

    all_administrators = api.get_users(company_id=company_id, role=Role(2))
    administrators = []

    for administrator in all_administrators:
        administrators.append((administrator, _get_avatar(administrator.avatar)))

    all_employees = api.get_users(company_id=company_id, role=Role(1))
    employees = []

    for employee in all_employees:
        employees.append((employee, _get_avatar(employee.avatar)))

    is_administrator = api.is_administrator(user.id, company_id)
    is_employee = api.is_employee(user.id, company_id)

    check = request.GET.get("login") == owner
    show = not check or company != None

    return render(request, 'trans/contacts.html', {'company': company, 'administrators': administrators, 'is_administrator': is_administrator, 'is_employee': is_employee, 'employees': employees, 'show': show, 'nickname': user.nickname, 'my_company': is_add_car(user) })


def car_park(request, company_id):
    api = get_api()

    owner = request.user.username
    user = api.get_user(nickname=owner)

    company = api.get_company(company_id=company_id)
    is_administrator = api.is_administrator(user.id, company_id)

    check = request.GET.get("login") == owner
    show = not check or company != None

    temp_cars = api.get_cars(company_id)
    cars = []

    for car in temp_cars:
        body_type = _get_body_type(car.body_type)

        cars.append((body_type, DOWNLOAD_TYPE[int(car.download_type)], car))

    return render(request, 'trans/car_park.html', {'company': company, 'show': show, 'is_administrator': is_administrator, 'cars': cars, 'my_company': is_add_car(user) })


def _get_body_type(car_body_type):
    body_type = int(str(car_body_type)[0])
    return BODY_TYPE[(int(_type(body_type) + int(str(car_body_type)[1:])))]


def _type(body_type):
    return {
        1: 0,
        2: len(BODY_TYPE_COVERED),
        3: len(BODY_TYPE_COVERED) + len(BODY_TYPE_UNCOVERED),
        4: len(BODY_TYPE_COVERED) + len(BODY_TYPE_UNCOVERED) + len(BODY_TYPE_TANK)
    }[body_type]



def add_employee(request, company_id):
    api = get_api()
    owner = request.user.username
    user = api.get_user(nickname=owner)

    company = api.get_company(company_id=company_id)
    is_administrator = api.is_administrator(user.id, company_id)

    check = request.GET.get("login") == owner
    show = not check or company != None

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['login']
            check_user, check_company = api.add_user_to_company(owner, nickname, company_id)

            if check_user and check_company:
                return redirect('/company/' + company_id + '/contacts')
            elif not check_user:
                error = "Пользователь с данным логином не зарегистрирован на сайте."
                return render(request, 'trans/add_employee.html', {'company': company, 'show': show, 'error': error})
            elif not check_company:
                error = "Пользователь уже состоит в предприятии."
                return render(request, 'trans/add_employee.html', {'company': company, 'show': show, 'error': error})

    return render(request, 'trans/add_employee.html', {'company': company, 'show': show, 'is_administrator': is_administrator, 'my_company': is_add_car(user) })


def change_administrator(request, company_id, user_id):
    if request.is_ajax():
        api = get_api()
        owner = request.user.username

        api.administrator(owner, user_id)

        message = user_id
    else:
        message = "Страницы не существует"
    return HttpResponse(message)


def remove_employee(request, company_id, user_id):
    if request.is_ajax():
        api = get_api()
        owner = request.user.username

        api.remove_user_from_company(owner, company_id, user_id)

        message = user_id
    else:
        message = "Страницы не существует"
    return HttpResponse(message)


def log(request, company_id):
    api = get_api()

    owner = request.user.username
    user = api.get_user(nickname=owner)

    company = api.get_company(company_id=company_id)
    is_administrator = api.is_administrator(user.id, company_id)

    check = request.GET.get("login") == owner
    show = not check or company != None

    logs = []
    temp_logs = api.get_logs(company_id)

    for log in temp_logs:
        user = api.get_user(nickname=log.username)
        avatar = _get_avatar(user.avatar)

        logs.append((log, user, log.date.strftime("%d.%m.%Y, %H:%M"), avatar))

    logs.reverse()

    return render(request, 'trans/company_log.html', {'company': company, 'show': show, 'logs': logs, 'is_administrator': is_administrator, 'my_company': is_add_car(user) })


def add_car(request, company_id):
    api = get_api()

    owner = request.user.username
    user = api.get_user(nickname=owner)

    company = api.get_company(company_id=company_id)
    is_administrator = api.is_administrator(user.id, company_id)

    check = request.GET.get("login") == owner
    show = not check or company != None
    form = None

    current_date = str(datetime.now().date())

    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form, check = _check_car_form(form)

            if check:
                api.create_car(
                    owner,
                    int(company_id),
                    form.cleaned_data['body_type'],
                    form.cleaned_data['download_type'],
                    form.cleaned_data['carrying_capacity'],
                    form.cleaned_data['volume'],
                    form.cleaned_data['loading_date_from'],
                    form.cleaned_data['loading_date_by'],
                    form.cleaned_data['country_loading'],
                    form.cleaned_data['country_unloading'],
                    note=form.cleaned_data['note']
                )
                return redirect('/company/'+ company_id + '/carpark')

    return render(request, 'trans/add_car.html', {'form': form, 'company': company, 'show': show, 'is_administrator': is_administrator, 'body_type_covered': BODY_TYPE_COVERED, 'body_type_uncovered': BODY_TYPE_UNCOVERED, 'body_type_tank': BODY_TYPE_TANK, 'body_type_special': BODY_TYPE_SPECIAL, 'download_types': DOWNLOAD_TYPE, 'current_date': current_date, 'my_company': is_add_car(user)})


def _check_car_form(form, extra=True, weigh=False):
    check = True
    if (form.cleaned_data['loading_date_from'] > form.cleaned_data['loading_date_by'] or
        form.cleaned_data['loading_date_by'].date() < pytz.utc.localize(datetime.utcnow()).date()):
        form.add_error('loading_date_from', "Неверный интервал времени.")
        check = False
    if int(form.cleaned_data['body_type']) < 0 and extra:
        form.add_error('body_type', "Тип кузова не выбран.")
        check = False
    if int(form.cleaned_data['download_type']) < 0 and extra:
        form.add_error('download_type', "Тип загрузки не выбран.")
        check = False
    try:
        if weigh:
            temp = int(form.cleaned_data['weigh'])
        else:
            temp = int(form.cleaned_data['carrying_capacity'])
    except ValueError as e:
        print(weigh, 12312312312312312312)
        if weigh:
            form.add_error('weigh', "Неверный формат ввода.")
        else:
            form.add_error('carrying_capacity', "Неверный формат ввода.")
        check = False
    try:
        temp = int(form.cleaned_data['volume'])
    except ValueError as e:
        form.add_error('volume', "Неверный формат ввода.")
        check = False

    return form, check


def edit_car(request, company_id, car_id):
    api = get_api()

    owner = request.user.username
    user = api.get_user(nickname=owner)

    company = api.get_company(company_id=company_id)
    is_administrator = api.is_administrator(user.id, company_id)

    check = request.GET.get("login") == owner
    show = not check or company != None

    car = api.get_car(car_id)

    current_body_type = _get_body_type(car.body_type)
    current_download_type = DOWNLOAD_TYPE[int(car.download_type)]
    loading_date_from = str(car.loading_date_from.date())
    loading_date_by = str(car.loading_date_by.date())

    form = CarForm()

    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form, check = _check_car_form(form, False)

            if check:
                api.edit_car(
                    owner,
                    int(company_id),
                    car.id,
                    body_type=form.cleaned_data['body_type'] if int(form.cleaned_data['body_type']) >= 0 else car.body_type,
                    download_type=form.cleaned_data['download_type'] if int(form.cleaned_data['download_type']) >= 0 else car.download_type,
                    carrying_capacity=form.cleaned_data['carrying_capacity'],
                    volume=form.cleaned_data['volume'],
                    loading_date_from=form.cleaned_data['loading_date_from'],
                    loading_date_by=form.cleaned_data['loading_date_by'],
                    country_loading=form.cleaned_data['country_loading'],
                    country_unloading=form.cleaned_data['country_unloading'],
                    note=form.cleaned_data['note']
                )
                return redirect('/company/'+ company_id + '/carpark')

    return render(request, 'trans/edit_car.html', {'form': form, 'company': company, 'show': show, 'is_administrator': is_administrator, 'body_type_covered': BODY_TYPE_COVERED, 'body_type_uncovered': BODY_TYPE_UNCOVERED, 'body_type_tank': BODY_TYPE_TANK, 'body_type_special': BODY_TYPE_SPECIAL, 'download_types': DOWNLOAD_TYPE, 'current_body_type': current_body_type, 'current_download_type': current_download_type, 'car': car, 'loading_date_from':loading_date_from, 'loading_date_by': loading_date_by, 'my_company': is_add_car(user) })


def remove_car(request, company_id, car_id):
    if request.is_ajax():
        api = get_api()
        owner = request.user.username

        api.delete_car(owner, company_id, car_id)

        message = car_id
    else:
        message = "Страницы не существует"
    return HttpResponse(message)


def like(request, company_id):
    if request.is_ajax():
        api = get_api()

        user = api.get_user(nickname=request.user.username)
        has_already_rated = api.has_already_rated(company_id, user.id)

        if not has_already_rated:
            api.create_review(
                3,
                None,
                company_id,
                user.id
            )
        else:
            api.change_rating(company_id, user.id, 3)

        message = "OK"
    else:
        message = "Страницы не существует"
    return HttpResponse(message)

def dislike(request, company_id):
    if request.is_ajax():
        api = get_api()

        user = api.get_user(nickname=request.user.username)
        has_already_rated = api.has_already_rated(company_id, user.id)

        if not has_already_rated:
            review_id = api.create_review(
                1,
                None,
                company_id,
                user.id
            )
        else:
            api.change_rating(company_id, user.id, 1)

        message = "OK"
    else:
        message = "Страницы не существует"
    return HttpResponse(message)


def verification(request, company_id, review_id):
    if request.is_ajax():
        api = get_api()
        user = api.get_user(nickname=request.user.username)

        review = api.get_review(company_id, user.id, review_id)

        if review.id == int(review_id):
            message = "OK"
        else:
            message = "ERROR"
    else:
        message = "Страницы не существует"

    return HttpResponse(message)


def edit_review(request, company_id, review_id):
    if request.is_ajax():
        api = get_api()
        user = api.get_user(nickname=request.user.username)
        print(review_id)

        review = api.get_review(company_id, user.id, review_id)
        text = request.GET.get('text')

        if review.id == int(review_id) and len(text) > 0:
            api.edit_review(company_id, user.id, text)
            message = "OK"
        else:
            message = "ERROR"
    else:
        message = "Страницы не существует"

    return HttpResponse(message)


def remove_review(request, company_id, review_id):
    if request.is_ajax():
        api = get_api()
        user = api.get_user(nickname=request.user.username)

        review = api.get_review(company_id, user.id)

        if review.id == int(review_id):
            api.delete_review(company_id, user.id)
            message = "OK"
        else:
            message = "ERROR"
    else:
        message = "Страницы не существует"

    return HttpResponse(message)


def _get_avatar(sender):
    return str(base64.b64encode(sender))[2: -1]

def message(request):
    api = get_api()
    sender = api.get_user(nickname=request.user.username)
    user_id = request.GET.get('sel')

    if user_id:
        recipient = api.get_user(user_id=user_id)

        all_messages = api.get_messages(sender.id, recipient.id)
        messages = []

        for message in all_messages:
            sender = api.get_user(message.sender_id)
            recipient = api.get_user(message.recipient_id)
            avatar = _get_avatar(sender.avatar)

            messages.append((message, sender, recipient, message.date.strftime("%d.%m.%Y, %H:%M"), avatar))

        recipient = recipient if recipient.id == int(user_id) else sender

        avatar = _get_avatar(recipient.avatar)

        return render(request, 'trans/message.html', {'recipient': recipient, 'messages': messages, 'recipient': recipient, 'avatar': avatar, 'my_company': is_add_car(sender)})
    elif sender:
        dialogs = api.get_messages(sender.id, distinct=True)
        my_avatar = _get_avatar(sender.avatar)

        messages = []

        for message in dialogs:
            recipient = api.get_user(message.recipient_id) if message.recipient_id != sender.id else api.get_user(message.sender_id)
            date = message.date.strftime("%d.%m.%Y, %H:%M")
            is_avatar = True if message.sender_id == sender.id else False
            avatar = _get_avatar(recipient.avatar)

            messages.append((message, recipient, date, is_avatar, avatar))

        return render(request, 'trans/list_message.html', {'messages': messages, 'my_avatar': my_avatar, 'my_company': is_add_car(sender) })
    else:
        return render(request, 'trans/list_message.html')


def message_send(request):
    if request.is_ajax():
        api = get_api()
        sender = api.get_user(nickname=request.user.username)
        recipient_id = request.GET.get('sel')
        text = request.GET.get('text')

        api.create_message(sender.id, recipient_id, text)
        message = "OK"
    else:
        message = "Страницы не существует"

    return HttpResponse(message)

def add_goods(request):
    api = get_api()

    owner = request.user.username
    user = api.get_user(nickname=owner)

    form = None

    current_date = str(datetime.now().date())

    if request.method == 'POST':
        form = GoodsForm(request.POST)
        if form.is_valid():
            form, check = _check_car_form(form, weigh=True)

            if check:
                api.create_goods(
                    user.id,
                    form.cleaned_data['name'],
                    form.cleaned_data['body_type'],
                    form.cleaned_data['car_count'],
                    form.cleaned_data['download_type'],
                    form.cleaned_data['belt_count'],
                    form.cleaned_data['weigh'],
                    form.cleaned_data['volume'],
                    form.cleaned_data['loading_date_from'],
                    form.cleaned_data['loading_date_by'],
                    form.cleaned_data['country_loading'],
                    form.cleaned_data['country_unloading'],
                    form.cleaned_data['rate'],
                    form.cleaned_data['price'],
                    form.cleaned_data['form_price'],
                    note=form.cleaned_data['note']
                )
                return redirect('/')

    return render(request, 'trans/add_goods.html', {'form': form, 'body_type_covered': BODY_TYPE_COVERED, 'body_type_uncovered': BODY_TYPE_UNCOVERED, 'body_type_tank': BODY_TYPE_TANK, 'body_type_special': BODY_TYPE_SPECIAL, 'download_types': DOWNLOAD_TYPE, 'prices': PRICES, 'form_prices': FORM_PRICES, 'my_company': is_add_car(user)})


def list_goods(request):
    api = get_api()
    user = api.get_user(nickname=request.user.username)

    search_goods = api.get_search_goods()
    goods = []

    for _goods in search_goods:
        date = _goods.get_date()

        body_type = _get_body_type(_goods.body_type)
        download_type = DOWNLOAD_TYPE[int(_goods.download_type)]

        car = body_type + ", " + download_type

        this_goods = [_goods.name, str(_goods.weigh) + " т., " + str(_goods.volume) + " м³"]

        price = [str(_goods.rate) + " " + PRICES[int(_goods.price)], FORM_PRICES[int(_goods.form_price)]]

        user = api.get_user(user_id=_goods.user_id)

        goods.append((_goods, date, car, this_goods, price, user))

    return render(request, 'trans/list_goods.html', {'search_goods': goods, 'my_company': is_add_car(user)})


def list_car(request):
    api = get_api()

    search_cars = api.get_cars()
    cars = []

    for car in search_cars:
        date = car.get_date()

        body_type = _get_body_type(car.body_type)
        download_type = DOWNLOAD_TYPE[int(car.download_type)]

        car_info = body_type + ", " + download_type

        # price = [str(car.rate) + " " + PRICES[int(car.price)], FORM_PRICES[int(car.form_price)]]

        # user = api.get_user(user_id=car.user_id)

        cars.append((car, date, car_info))

    return render(request, 'trans/list_car.html', {'cars': cars})


def write_file(text):
    with open("output.txt", "w") as file:
        file.write(str(text))