from django.conf.urls import url
from . import views

app_name = 'collab'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.ProjectView.as_view(), name='project'),
    url(r'project/add/$', views.ProjectCreate.as_view(), name='project-add'),
    url(r'project/update/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='project-update'),
    url(r'project/(?P<pk>[0-9]+)/delete/$', views.ProjectDelete.as_view(), name='project-delete'),
    url(r'match/(?P<pk>[0-9]+)/delete/$', views.MatchDelete.as_view(), name='match-delete'),

]
