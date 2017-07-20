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

    # putting Match objects from project in view ordered by rank
    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        # only load if self.request.user == founder
        if self.request.user.id is self.get_object().founder.id:
            context['match_list'] = Match.objects.filter(project=self.object.id).order_by('-rank')
        return context


class ProjectCreate(AuthRequiredMixin, CreateView):
    # form_class = ProjectCreateForm
    model = Project
    fields = ['title', 'city', 'description', 'skills_needed']

    def generate_matches(self, form):
        # grabs project skills
        p_skills = Tag.objects.filter(project__id=form.instance.id)
        # grabs project city
        p_city = Project.objects.filter(id=form.instance.id).values('city')
        # grabs users by matching skills and location, excludes project creator
        user_list = User.objects.filter(userprofile__skills__in=p_skills
                                        ).filter(userprofile__city=p_city
                                                 ).exclude(id=form.instance.founder.id)
        # puts users in dict by their frequency in queryset
        dict = {}
        for u in user_list:
            if not u in dict:
                dict[u] = 1
            else:
                dict[u] += 1
        # converts user into match obj with frequency as rank
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

    def form_valid(self, form):
        form.save()
        # skills needed always shows up as changed
        print ('skills_needed' in form.changed_data), 'expecting t or f'
        # regenerates project matches
        # need to clear old matches first
        # ProjectCreate().generate_matches(form)
        return super(ProjectUpdate, self).form_valid(form)


class ProjectDelete(UserAuthMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('accounts:dashboard')


class MatchDelete(UserAuthMixin, DeleteView):
    model = Match
    success_url = reverse_lazy('accounts:dashboard')

