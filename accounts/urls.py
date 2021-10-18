from django.conf.urls import url
from . import views
from accounts.views import logout_view

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'profile/(?P<slug>[\w.@+-]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'profile/update/(?P<pk>[0-9]+)/$', views.ProfileSocialUpdate.as_view(), name='profile-update'),
    url(r'request/send/(?P<project_id>[0-9]+)/$', views.sendrequest, name='request-send'),
]
