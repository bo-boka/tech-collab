# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse_lazy
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

    def generate_matches(self, form):
        """
        Gets project skills and city, finds users with those skills that live in the same city
        and creates Match object with a rank of how many skills the user matched to the project.
        :param form: project model form
        :return: None
        """
        # grabs project skills & city
        p_skills = Tag.objects.filter(project__id=form.instance.id)
        p_city = Project.objects.filter(id=form.instance.id).values('city')[0]['city']

        # grabs users by matching skills and location, excludes project creator
        user_list = User.objects.filter(userprofile__skills__in=p_skills
                                        ).filter(userprofile__city=p_city
                                                 ).exclude(id=form.instance.founder.id)

        # puts users in dict by their frequency (# matched skills) in queryset
        dict = {}
        for u in user_list:
            if u not in dict:
                dict[u] = 1
            else:
                dict[u] += 1

        # converts user into match obj with frequency as rank
        for key, value in dict.items():
            m = Match(user=key, project=form.instance, rank=value)
            m.save()

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
        self.generate_matches(form)
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

