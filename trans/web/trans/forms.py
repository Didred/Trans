from datetime import datetime
from dateutil.relativedelta import relativedelta

from django import forms
from django.contrib.auth import password_validation
import unicodedata
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from . import get_api
from library.models.review import Rating


DATE_FORMAT = '%Y-%m-%d %H:%M'


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))


class EditUserForm(forms.Form):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    phone = forms.CharField(max_length=30)


class CompanyForm(forms.Form):
    name = forms.CharField(max_length=30)
    UNP = forms.CharField(max_length=30)
    primary_occupation = forms.CharField(max_length=30)
    license = forms.CharField(max_length=30)
    country = forms.CharField(max_length=30)
    town = forms.CharField(max_length=30)
    address = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    description = forms.CharField(max_length=10000)


FRUIT_CHOICES= [
    (1, 'Отрицательный'),
    (2, 'Нейтральный'),
    (3, 'Положительный'),
    ]

class ReviewForm(forms.Form):
    rating = forms.CharField(widget=forms.RadioSelect(choices=FRUIT_CHOICES))
    review = forms.CharField(max_length=10000)


class UserForm(forms.ModelForm):
    # def __init__(self, nickname, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username", "surname",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
