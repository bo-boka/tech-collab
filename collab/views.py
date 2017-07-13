# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from collab.models import Project
from collab.models import Match
from taggit.models import Tag
from django.contrib.auth.models import User
from collab.mixins import UserAuthMixin, AuthRequiredMixin
# from .forms import ProjectCreateForm
# from django.contrib.auth.decorators import login_required


class HomeView(generic.ListView):
    template_name = 'collab/home.html'
    queryset = Project.objects.filter(archived=False)


class ProjectView(generic.DetailView):
    model = Project
    template_name = 'collab/project.html'


class ProjectCreate(AuthRequiredMixin, CreateView):
    # form_class = ProjectCreateForm
    model = Project
    fields = ['title', 'city', 'description', 'skills_needed']

    def generate_matches(self, form):

        # form['skills_needed']  # returns boundwidget that needs parsing
        # id = form.instance.id
        p_skills = Tag.objects.filter(project__id=form.instance.id)
        user_list = User.objects.filter(userprofile__skills__in=p_skills)

        dict = {}
        for u in user_list:
            if not u in dict:
                dict[u] = 1
            else:
                dict[u] += 1
        for key, value in dict.iteritems():
            print key, value
            m = Match(user=key, project=form.instance, rank=value)
            m.save()

    def form_valid(self, form):
        form.instance.founder = self.request.user
        form.save()
        self.generate_matches(form)
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(UserAuthMixin, UpdateView):
    model = Project
    fields = ['title', 'city', 'description', 'skills_needed', 'archived']


class ProjectDelete(UserAuthMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('accounts:dashboard')

