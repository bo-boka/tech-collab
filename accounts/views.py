# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (
    authenticate,
    login,
    logout,)
from .forms import UserRegForm, SocialUserFormSet
from .forms import UserLoginForm
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from collab.models import Project
from django.contrib.auth.models import User
from accounts.models import UserProfile
from accounts.models import Request
from collab.models import Match
from collab.mixins import UserAuthMixin


# adds inline form for social networks in update user profile
class ProfileSocialCreate(CreateView):
    model = UserProfile
    fields = ['platform', 'url']
    success_url = reverse_lazy('accounts:dashboard')

    def get_context_data(self, **kwargs):
        data = super(ProfileSocialCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['usersocials'] = SocialUserFormSet(self.request.POST)
        else:
            data['usersocials'] = SocialUserFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        usersocials = context['usersocials']
        with transaction.atomic():
            self.object = form.save()

            if usersocials.is_valid():
                usersocials.instance = self.object
                usersocials.save()
        return super(ProfileSocialCreate, self).form_valid(form)


# profile view w username slug
class ProfileView(generic.DetailView):
    model = User
    slug_field = "username"
    template_name = 'accounts/profile.html'


class ProfileUpdate(UpdateView):
    model = UserProfile
    fields = ['city', 'zip', 'skills', 'phone', 'picture', 'bio', 'experience', 'availability']


class DashboardView(generic.ListView):
    template_name = 'accounts/dashboard.html'
    context_object_name = 'project_list'
    model = Project

    # add request obj list to view
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'request_list': Request.objects.filter(recipient=self.request.user),
            # 'more_context': Request.objects.all(),
        })
        return context

    def get_queryset(self):
        return Project.objects.filter(founder=self.request.user)


# get project_id, match_id, and add request w sender as user.request
def sendrequest(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    try:
        recipient = get_object_or_404(User, pk=request.POST['recipient_id'])

    except (KeyError, Match.DoesNotExist):
        return render(request, 'accounts/dashboard.html', {
            'project': project,
            'error_message': "You did not select a valid recipient",
        })
    else:
        # create request obj
        sender = request.user
        req = Request(project=project, sender=sender, recipient=recipient, message="Let's work together")
        req.save()
        return redirect('accounts:dashboard')


def logout_view(request):
    logout(request)
    return redirect('home')


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            print(request.user.is_authenticated()), 'yippy'
            return redirect('accounts:dashboard')
        return render(request, self.template_name, {'form': form})


class RegisterView(View):
    form_class = UserRegForm
    template_name = 'accounts/registration_form.html'

    # since using same url for get and post reqs

    # display blank form w get
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # storing locally first before putting in DB
            user = form.save(commit=False)
            # format
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # encrypt pswd
            user.set_password(password)
            # now save
            user.save()
            # authenticate and login user
            user = authenticate(username=username, password=password)
            if user is not None:
                # if account isn't banned or something
                if user.is_active:
                    login(request, user)
                    return redirect('accounts:dashboard')
        # else not auth, sent blank for back again
        return render(request, self.template_name, {'form': form})
