# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from accounts.forms import UserForm
from accounts.forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.views.generic import View


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
    return render(request, "login.html", {"form": form, "title": title})


# def register_view(request):
#     return render(request, "form.html", {})

def logout_view(request):
    return render(request, "form.html", {})


class UserFormView(View):
    form_class = UserForm
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
