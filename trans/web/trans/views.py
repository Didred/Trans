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
    CarForm
)
from library.models.user import Role

from datetime import datetime
import pytz
import math

FIELDS = [
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


def home(request):
    api = get_api()
    all_companys = api.get_companys()
    companys = []

    user = api.get_user(nickname=request.user.username)

    for company in all_companys:
        rating = api.get_ratings(company.id)
        review = api.get_review(company.id, user.id) if user else None

        companys.append((company, rating[0], rating[1], rating[2], True if review else False))

    return render(request, 'trans/home.html', {'fields': FIELDS, 'companys': companys})


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
    owner = request.user.username

    user = api.get_user(nickname=nickname)
    company = api.get_company(company_id=user.company_id)
    is_administrator = False
    if company:
        is_administrator = api.is_administrator(user.id, company.id)

    check = nickname == owner
    show = not check or company != None

    return render(request, 'trans/profile.html', {'member': user, 'company': company, 'check': check, 'show': show, 'is_administrator': is_administrator})


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
                FIELDS[int(form.cleaned_data['primary_occupation'])],
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

    return render(request, 'trans/add_company.html', {'form': form, 'fields': FIELDS})


def edit_profile(request):
    api = get_api()
    user = request.user.username

    if request.method == 'POST':
        form = EditUserForm(request.POST)
        if form.is_valid():
            api.edit_user(
                user,
                form.cleaned_data['name'],
                form.cleaned_data['surname'],
                form.cleaned_data['email'],
                form.cleaned_data['phone'],
            )
            return redirect('/profile/' + user)

    else:
        member = api.get_user(nickname=user)

    return render(request, 'trans/edit_profile.html', {'form': member})


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
        number = FIELDS.index(company.primary_occupation)

    return render(request, 'trans/edit_company.html', {'form': company, 'fields': FIELDS, 'number': number})


def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/profile/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'trans/change_password.html', {'form': form})


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

    return render(request, 'trans/add_review.html', {'form': form, 'company': company})


def get_review(request, company_id):
    api = get_api()
    user = request.user.username

    company = api.get_company(company_id=company_id)
    company_reviews = api.get_reviews(company_id)
    negative, neutral, positive = api.get_company_rating(company_id)
    reviews = []

    for review in company_reviews:
        if review.review is not None:
            reviews.append((review, api.get_user(user_id=review.user_id), review.date.strftime("%d.%m.%Y, %H:%M")))

    return render(
        request, 'trans/review.html',
        {
            'reviews': reviews,
            'company': company,
            'negative': negative,
            'neutral': neutral,
            'positive': positive,
            'nickname': user
        })


def contacts(request, company_id):
    api = get_api()

    owner = request.user.username
    user = api.get_user(nickname=owner)

    company = api.get_company(company_id=company_id)

    administrators = api.get_users(company_id=company_id, role=Role(2))
    employees = api.get_users(company_id=company_id, role=Role(1))

    is_administrator = api.is_administrator(user.id, company_id)
    is_employee = api.is_employee(user.id, company_id)

    check = request.GET.get("login") == owner
    show = not check or company != None

    return render(request, 'trans/contacts.html', {'company': company, 'administrators': administrators, 'is_administrator': is_administrator, 'is_employee': is_employee, 'employees': employees, 'show': show, 'nickname': user.nickname })


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

    return render(request, 'trans/car_park.html', {'company': company, 'show': show, 'is_administrator': is_administrator, 'cars': cars })


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

    return render(request, 'trans/add_employee.html', {'company': company, 'show': show, 'is_administrator': is_administrator })


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
        logs.append((log, user, log.date.strftime("%d.%m.%Y, %H:%M")))

    logs.reverse()

    return render(request, 'trans/company_log.html', {'company': company, 'show': show, 'logs': logs, 'is_administrator': is_administrator })


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

    return render(request, 'trans/add_car.html', {'form': form, 'company': company, 'show': show, 'is_administrator': is_administrator, 'body_type_covered': BODY_TYPE_COVERED, 'body_type_uncovered': BODY_TYPE_UNCOVERED, 'body_type_tank': BODY_TYPE_TANK, 'body_type_special': BODY_TYPE_SPECIAL, 'download_types': DOWNLOAD_TYPE, 'current_date': current_date})


def _check_car_form(form, extra=True):
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
        temp = int(form.cleaned_data['carrying_capacity'])
    except ValueError as e:
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

    return render(request, 'trans/edit_car.html', {'form': form, 'company': company, 'show': show, 'is_administrator': is_administrator, 'body_type_covered': BODY_TYPE_COVERED, 'body_type_uncovered': BODY_TYPE_UNCOVERED, 'body_type_tank': BODY_TYPE_TANK, 'body_type_special': BODY_TYPE_SPECIAL, 'download_types': DOWNLOAD_TYPE, 'current_body_type': current_body_type, 'current_download_type': current_download_type, 'car': car, 'loading_date_from':loading_date_from, 'loading_date_by': loading_date_by })


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

def message(request):
    api = get_api()
    sender = api.get_user(nickname=request.user.username)
    user_id = request.GET.get('sel')
    recipient = api.get_user(user_id=user_id)

    messages = api.get_messages(sender.id, recipient.id)

    return render(request, 'trans/message.html', {'recipient': recipient, 'messages': messages})


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

def write_file(text):
    with open("output.txt", "w") as file:
        file.write(str(text))