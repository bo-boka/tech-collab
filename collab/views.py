# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from collab.models import Project, Match
from taggit.models import Tag
from django.contrib.auth.models import User
from collab.mixins import UserAuthMixin, AuthRequiredMixin
from .tc_lib import generate_matches
# from .forms import ProjectCreateForm
# from django.contrib.auth.decorators import login_required


class HomeView(generic.ListView):
    """
    Home Page View
    """
    template_name = 'collab/home.html'
    queryset = Project.objects.filter(archived=False)


class ProjectView(generic.DetailView):
    """
    Project Page View
    """
    model = Project
    template_name = 'collab/project.html'

    def get_context_data(self, **kwargs):
        """
        Puts User Matches in view, in order by rank (# of matching skills)
        :param kwargs:
        :return:
        """
        context = super(ProjectView, self).get_context_data(**kwargs)
        # only load if self.request.user == founder
        if self.request.user.id is self.get_object().founder.id:
            context['match_list'] = Match.objects.filter(project=self.object.id).order_by('-rank')
        return context


class ProjectCreate(AuthRequiredMixin, CreateView):
    """
    Project Create Form
    """
    # form_class = ProjectCreateForm
    model = Project
    fields = ['title', 'city', 'description', 'skills_needed']

    def form_valid(self, form):
        """
        Adds founder to the project model form, saves the project in the database, calls the
        generate_matches() function to find & save project-user matches, and redirects to the
        newly created project.
        :param form: project model form
        :return: project.html page
        """
        form.instance.founder = self.request.user
        form.save()
        generate_matches(form)
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(UserAuthMixin, UpdateView):
    """
    Project Update Form
    """
    model = Project
    fields = ['title', 'city', 'description', 'skills_needed', 'archived']

    def form_valid(self, form):
        form.save()
        # skills needed always shows up as changed
        print('skills_needed' in form.changed_data), 'expecting t or f'
        # regenerates project matches
        # need to clear old matches first
        # ProjectCreate().generate_matches(form)
        return super(ProjectUpdate, self).form_valid(form)


class ProjectDelete(UserAuthMixin, DeleteView):
    """
    Project deletion functionality via an icon on the user's dashboard
    """
    model = Project
    success_url = reverse_lazy('accounts:dashboard')


class MatchDelete(UserAuthMixin, DeleteView):
    """
    Match deletion functionality via an icon on the Matches dropdown on the Project
    """
    model = Match
    success_url = reverse_lazy('accounts:dashboard')

