from django.conf.urls import url
from . import views
from accounts.views import logout_view

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),

    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),

    # profile c
    url(r'profile/add/$', views.ProfileCreate.as_view(), name='profile-add'),

    # profile view self
    url(r'^(?P<slug>[\w.@+-]+)/$', views.ProfileViewSelf.as_view(), name='profile'),

    # profile view other user
    # url(r'profile/^(?P<slug>[\w.@+-]+)/$', views.ProfileViewPublic.as_view(), name='profile-public'),

    # profile view update
    url(r'profile/update/^(?P<slug>[\w.@+-]+)/$', views.ProfileUpdate.as_view(), name='profile-update'),
]
