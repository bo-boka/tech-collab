from django.conf.urls import url
from . import views
from accounts.views import logout_view

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
]
