# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm
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


class UserFormView(View):
    form_class = UserForm
    template_name = 'collab/registration_form.html'

    # since using same url for get and post reqs

    # display blank for w get
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # storing locally first before putting in DB
            user = form.save(commit=False)

            # first we want to get cleaned(normalized) data
                # which is data that is formatted properly
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # when changing password, need to use func for encryption
            user.set_password(password)
            # now save
            user.save()

            # authenticate and login user
            # returns User obj if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                # if account isn't banned or something
                if user.is_active:
                    login(request, user)
                    return redirect('home')
        # else not auth, sent blank for back again
        return render(request, self.template_name, {'form': form})