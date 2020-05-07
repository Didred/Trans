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
    EmployeeForm
)
from library.models.user import Role

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


def home(request):
    api = get_api()
    companys = api.get_companys()

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
    check = nickname == owner
    show = not check or company != None

    return render(request, 'trans/profile.html', {'member': user, 'company': company, 'check': check, 'show': show})


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

    company = api.get_company(company_id=company_id)
    company_reviews = api.get_reviews(company_id)
    negative, neutral, positive = api.get_company_rating(company_id)
    reviews = []

    for review in company_reviews:
        reviews.append((review, api.get_user(user_id=review.user_id), review.date.strftime("%d.%m.%Y, %H:%M")))

    return render(
        request, 'trans/review.html',
        {
            'reviews': reviews,
            'company': company,
            'negative': negative,
            'neutral': neutral,
            'positive': positive
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

    company = api.get_company(company_id=company_id)

    check = request.GET.get("login") == owner
    show = not check or company != None

    return render(request, 'trans/car_park.html', {'company': company, 'show': show })


def add_employee(request, company_id):
    api = get_api()
    owner = request.user.username
    user = api.get_user(nickname=owner)

    company = api.get_company(company_id=company_id)

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

    return render(request, 'trans/add_employee.html', {'company': company, 'show': show})


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

    company = api.get_company(company_id=company_id)

    check = request.GET.get("login") == owner
    show = not check or company != None

    logs = []
    temp_logs = api.get_logs(company_id)

    for log in temp_logs:
        user = api.get_user(nickname=log.username)
        logs.append((log, user, log.date.strftime("%d.%m.%Y, %H:%M")))

    logs.reverse()

    return render(request, 'trans/company_log.html', {'company': company, 'show': show, 'logs': logs })


def write_file(text):
    with open("output.txt", "w") as file:
        file.write(str(text))