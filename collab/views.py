# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Project
from models import Technology
from taggit.models import Tag
from django.contrib.auth.models import User
# from .forms import ProjectCreateForm
# from django.contrib.auth.decorators import login_required


class HomeView(generic.ListView):
    template_name = 'collab/home.html'

    def get_queryset(self):
        return Project.objects.all()


class ProjectView(generic.DetailView):
    model = Project
    template_name = 'collab/project.html'


class ProjectCreate(CreateView):
    # form_class = ProjectCreateForm
    model = Project
    fields = ['title', 'description', 'technologies', 'skills_needed']

    def generate_matches(self):

        # db queries to get matching users w matching project technologies

        # users returned by frequency at top of list
        # also try to return which techs the users matched on if possible
        # p_techs = Technology.objects.filter(project__id=self.id).values('id')
        # user_list = User.objects.filter(userprofile__technologies__in=p_techs)

        p_skills = Tag.objects.filter(project__id=self.id)  # or self.skills_needed??
        user_list = User.objects.filter(userprofile__skills__in=p_skills)

        # dict = []  # ??
        # for u in user_list:
        #     if u in dict:
        #

        # sort users based on frequency but will likely need to change matches to an ordered list

    def form_valid(self, form):
        form.instance.founder = self.request.user

        # parse technologies list, adding new ones to Technology model

        # self.object = form.save()
        # self.generate_matches()
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['title', 'description', 'technologies', 'collaborators', 'skills_needed']


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('home')

