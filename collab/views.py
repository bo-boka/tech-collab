# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Project


class HomeView(generic.ListView):
    template_name = 'collab/home.html'

    def get_queryset(self):
        return Project.objects.all()


class ProjectView(generic.DetailView):
    model = Project
    template_name = 'collab/project.html'


class ProjectCreate(CreateView):
    model = Project
    fields = ['title', 'description', 'technologies']


class ProjectUpdate(UpdateView):
    model = Project
    fields = []


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('home')

