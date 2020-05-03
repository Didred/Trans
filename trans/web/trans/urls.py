from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^$', views.home, name='home'),

    url(r'^login/$', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="trans/home.html"), name="logout"),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^profile/(?P<nickname>.+?)/$', views.profile, name='profile'),
    url(r'^add_company/$', views.add_company, name='add_company'),
    url(r'^profile/edit$', views.edit_profile, name='edit_profile'),
    url(r'^profile/edit/password$', views.edit_password, name='edit_password'),
    url(r'^profile/edit/company$', views.edit_company, name='edit_company'),
    url(r'^company/(?P<company_id>[0-9]+)/review/add$', views.add_review, name='add_review'),
    url(r'^company/(?P<company_id>[0-9]+)/review$', views.get_review, name='review'),
    url(r'^company/(?P<company_id>[0-9]+)/contacts$', views.contacts, name='contacts'),
    url(r'^company/(?P<company_id>[0-9]+)/carpark$', views.car_park, name='car_park'),
    url(r'^company/(?P<company_id>[0-9]+)/contacts/add$', views.add_employee, name='add_employee'),
]
