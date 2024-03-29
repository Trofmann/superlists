from django.urls import re_path
from django.contrib.auth.views import logout_then_login

from accounts import views

urlpatterns = [
    re_path(r'^send_login_email$', views.send_login_email, name='send_login_email'),
    re_path(r'^login$', views.login, name='login'),
    re_path(r'^logout$', logout_then_login, {'login_url': '/'}, name='logout')
]
