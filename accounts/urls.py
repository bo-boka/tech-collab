from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
from accounts.views import (login_view, logout_view)

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', login_view, name='login'),
]
