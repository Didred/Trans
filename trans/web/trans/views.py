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
    CompanyForm
)


def home(request):
    return render(request, 'trans/home.html')


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


def profile(request):
    api = get_api()
    user = api.get_user(nickname=request.user.username)
    company = api.get_company(nickname=request.user.username)
    write_file(company)

    return render(request, 'trans/profile.html', {'member': user, 'company': company})


def add_company(request):
    api = get_api()

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        write_file(form.is_valid())
        if form.is_valid():
            api.create_company(
                request.user.username,
                form.cleaned_data['UNP'],
                form.cleaned_data['name'],
                form.cleaned_data['primary_occupation'],
                form.cleaned_data['license'],
                form.cleaned_data['country'],
                form.cleaned_data['town'],
                form.cleaned_data['address'],
                form.cleaned_data['phone']
            )
            return redirect('/profile/')
    else:
        form = CompanyForm()

    return render(request, 'trans/add_company.html', {'form': form})


def write_file(text):
    with open("output.txt", "w") as file:
        file.write(str(text))
