from django.conf.urls import url
from . import views

app_name = 'collab'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.ProjectView.as_view(), name='project'),
    url(r'project/add/$', views.ProjectCreate.as_view(), name='project-add'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'project/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='project-update'),
    url(r'project/(?P<pk>[0-9]+)/delete/$', views.ProjectDelete.as_view(), name='project-delete'),
]
