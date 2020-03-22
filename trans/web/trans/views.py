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
    UserForm
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
    return render(request, 'trans/profile.html')
