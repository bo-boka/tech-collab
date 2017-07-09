from django.conf.urls import url
from . import views
from accounts.views import logout_view

app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),

    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),

    # profile create --- already created when user registers
    # url(r'profile/add/$', views.ProfileCreate.as_view(), name='profile-add'),

    # profile view using id
    # url(r'^(?P<pk>[0-9]+)/$', views.ProfileViewId.as_view(), name='profile-id'),

    # profile view update
    url(r'profile/update/(?P<pk>[0-9]+)/$', views.ProfileUpdate.as_view(), name='profile-update'),

    # profile view update with username slug --- doesn't work
    url(r'profile/update/(?P<slug>[\w.@+-]+)/$', views.ProfileUpdateUser.as_view(), name='profile-update-user'),

    # profile view user
    # slug is for User not UserProfile
    url(r'profile/(?P<slug>[\w.@+-]+)/$', views.ProfileView.as_view(), name='profile'),
]
