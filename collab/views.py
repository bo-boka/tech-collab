# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Project
from accounts.models import UserProfile
from models import Technology
from django.contrib.auth.models import User
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

    def generate_matches(self):
        proj_techs = self.technologies

        # db queries to get matching users w matching project technologies
        # gives repeat profiles
        # gives userprofile per matching tech rather than giving users that match all techs!!
            # maybe that could be good... users returned by frequency at top of list
            # also try to return which techs the users matched on if possible
        # and change to User rather than UserProfile probably
        p_techs = Technology.objects.filter(project__id=self.id).values('id')
        user_list = UserProfile.objects.filter(technologies__in=p_techs)

        # sort users based on frequency but will likely need to change matches to an ordered list

    def form_valid(self, form):
        form.instance.founder = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['title', 'description', 'technologies', 'collaborators']


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('home')

