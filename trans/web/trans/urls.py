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
    url(r'^company/(?P<company_id>[0-9]+)/carpark/add$', views.add_car, name='add_car'),
    url(r'^company/(?P<company_id>[0-9]+)/contacts/add$', views.add_employee, name='add_employee'),
    url(r'^company/(?P<company_id>[0-9]+)/change_administrator/(?P<user_id>[0-9]+)/$', views.change_administrator, name='change_administrator'),
    url(r'^company/(?P<company_id>[0-9]+)/remove_employee/(?P<user_id>[0-9]+)/$', views.remove_employee, name='remove_employee'),
    url(r'^company/(?P<company_id>[0-9]+)/log$', views.log, name='log'),
    url(r'^company/(?P<company_id>[0-9]+)/remove_car/(?P<car_id>[0-9]+)/$', views.remove_car, name='remove_car'),
    url(r'^company/(?P<company_id>[0-9]+)/carpark/(?P<car_id>[0-9]+)/edit$', views.edit_car, name='edit_car'),
    url(r'^company/(?P<company_id>[0-9]+)/like$', views.like, name='like'),
    url(r'^company/(?P<company_id>[0-9]+)/dislike$', views.dislike, name='dislike'),
    url(r'^company/(?P<company_id>[0-9]+)/review/(?P<review_id>[0-9]+)/verification/$', views.verification, name='verification'),
    url(r'^company/(?P<company_id>[0-9]+)/review/(?P<review_id>[0-9]+)/edit/$', views.edit_review, name='edit_review'),
    url(r'^company/(?P<company_id>[0-9]+)/remove_review/(?P<review_id>[0-9]+)/$', views.remove_review, name='remove_review'),
    url(r'^message$', views.message, name='message'),
    url(r'^send$', views.message_send, name='send'),

]
