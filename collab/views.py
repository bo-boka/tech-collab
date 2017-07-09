# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Project
from models import Technology
# from django.contrib.auth.decorators import login_required


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

    def form_valid(self, form):
        form.instance.founder = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['title', 'description', 'technologies', 'collaborators']


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('home')

