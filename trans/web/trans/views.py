from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm
)

from django.shortcuts import (
    render,
    redirect
)

from . import get_api
from .forms import (
    UserForm,
    EditUserForm,
    CompanyForm
)

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
    company = api.get_company(nickname=nickname)
    check = nickname == owner

    return render(request, 'trans/profile.html', {'member': user, 'company': company, 'check': check})


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
            return redirect('/profile/')

    else:
        member = api.get_user(nickname=user)

    return render(request, 'trans/edit_profile.html', {'form': member})


def edit_company(request):
    api = get_api()
    user = request.user.username
    company = ""

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        write_file(form.is_valid())
        if form.is_valid():
            api.edit_company(
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


def write_file(text):
    with open("output.txt", "w") as file:
        file.write(str(text))
