from datetime import datetime
from dateutil.relativedelta import relativedelta

from django import forms
from django.contrib.auth import password_validation
import unicodedata
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from . import get_api
from library.models.review import Rating


DATE_FORMAT = '%Y-%m-%d'


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))


class EditUserForm(forms.Form):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    phone = forms.CharField(max_length=30)
    avatar = forms.ImageField(required=False)


class CompanyForm(forms.Form):
    name = forms.CharField(max_length=25)
    UNP = forms.CharField(max_length=30)
    primary_occupation = forms.CharField(max_length=30)
    license = forms.CharField(max_length=30)
    country = forms.CharField(max_length=30)
    town = forms.CharField(max_length=30)
    address = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    description = forms.CharField(max_length=10000)


class CarForm(forms.Form):
    body_type = forms.CharField(max_length=30)
    download_type = forms.CharField(max_length=30)
    carrying_capacity = forms.CharField(max_length=30)
    volume = forms.CharField(max_length=30)
    loading_date_from = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime'},
            format=DATE_FORMAT
        ),
        initial=format(datetime.now(), DATE_FORMAT)
    )
    loading_date_by = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime'},
            format=DATE_FORMAT
        ),
        initial=format(datetime.now(), DATE_FORMAT)
    )
    country_loading = forms.CharField(max_length=300)
    country_unloading = forms.CharField(max_length=300)
    rate = forms.CharField(max_length=30)
    price = forms.CharField(max_length=30)
    form_price = forms.CharField(max_length=30)
    note = forms.CharField(max_length=10000, required=False)


class GoodsForm(forms.Form):
    name = forms.CharField(max_length=30)
    body_type = forms.CharField(max_length=30)
    car_count = forms.CharField(max_length=30)
    download_type = forms.CharField(max_length=30)
    belt_count = forms.CharField(max_length=30)
    weigh = forms.CharField(max_length=30)
    volume = forms.CharField(max_length=30)
    loading_date_from = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime'},
            format=DATE_FORMAT
        ),
        initial=format(datetime.now(), DATE_FORMAT)
    )
    loading_date_by = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime'},
            format=DATE_FORMAT
        ),
        initial=format(datetime.now(), DATE_FORMAT)
    )
    country_loading = forms.CharField(max_length=300)
    country_unloading = forms.CharField(max_length=300)
    rate = forms.CharField(max_length=30)
    price = forms.CharField(max_length=30)
    form_price = forms.CharField(max_length=30)
    note = forms.CharField(max_length=10000, required=False)


class SearchCarForm(forms.Form):
    body_type = forms.CharField(max_length=30, required=False)
    download_type = forms.CharField(max_length=30, required=False)
    carrying_capacity_min = forms.CharField(max_length=30, required=False, initial="")
    carrying_capacity_max = forms.CharField(max_length=30, required=False, initial="")
    volume_min = forms.CharField(max_length=30, required=False, initial="")
    volume_max = forms.CharField(max_length=30, required=False, initial="")
    loading_date_from = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime'},
            format=DATE_FORMAT
        ),
        required=False
    )
    loading_date_by = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime'},
            format=DATE_FORMAT
        ),
        required=False
    )
    country_loading = forms.CharField(max_length=300, required=False)
    country_unloading = forms.CharField(max_length=300, required=False)


class SearchGoodsForm(forms.Form):
    body_type = forms.CharField(max_length=30, required=False)
    download_type = forms.CharField(max_length=30, required=False)
    weigh_min = forms.CharField(max_length=30, required=False, initial="")
    weigh_max = forms.CharField(max_length=30, required=False, initial="")
    volume_min = forms.CharField(max_length=30, required=False, initial="")
    volume_max = forms.CharField(max_length=30, required=False, initial="")
    loading_date_from = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime'},
            format=DATE_FORMAT
        ),
        required=False
    )
    loading_date_by = forms.DateTimeField(
        widget=forms.widgets.DateInput(
            attrs={'type': 'datetime'},
            format=DATE_FORMAT
        ),
        required=False
    )
    country_loading = forms.CharField(max_length=300, required=False)
    country_unloading = forms.CharField(max_length=300, required=False)


CHOICES = [
    (1, 'Отрицательный'),
    (2, 'Нейтральный'),
    (3, 'Положительный'),
]


class ReviewForm(forms.Form):
    rating = forms.CharField(widget=forms.RadioSelect(choices=CHOICES))
    review = forms.CharField(max_length=10000)


class EmployeeForm(forms.Form):
    login = forms.CharField(max_length=20)


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
