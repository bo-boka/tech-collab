# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,)
from .forms import UserRegForm
from .forms import UserLoginForm
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from collab.models import Project
from django.contrib.auth.models import User
from accounts.models import UserProfile


class ProfileView(generic.DetailView):
    model = User
    slug_field = "username"
    template_name = 'accounts/profile.html'


class DashboardView(generic.ListView):
    template_name = 'accounts/dashboard.html'

    def get_queryset(self):
        return Project.objects.filter(founder=self.request.user)


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
                    return redirect('home')
        # else not auth, sent blank for back again
        return render(request, self.template_name, {'form': form})
