# # -*- coding: utf-8 -*-
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (
    authenticate,
    login,
    logout,)
from .forms import UserRegForm, UserLoginForm, SocialUserFormSet
from django.views.generic import View
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from accounts.models import UserProfile, Request
from collab.models import Match, Project
from collab.mixins import UserAuthMixin
from django.http import HttpResponseRedirect
import collab.tc_lib as tc_lib


class ProfileSocialUpdate(UpdateView):
    """
    Profile Create/Update Form
    """
    model = UserProfile
    fields = ['name', 'pronouns', 'city', 'skills', 'email', 'phone', 'picture', 'bio']

    def get_context_data(self, **kwargs):
        """
        Adds social media platforms formset to profile update form since they're on a related table
        and are not easily accessed via Class-Based-Views.
        :param kwargs:
        :return:
        """
        context_data = super(ProfileSocialUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context_data['usersocials'] = SocialUserFormSet(self.request.POST, instance=self.object)
        else:
            context_data['usersocials'] = SocialUserFormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        """
        Saves social media platforms to profile.
        :param form:
        :return:
        """
        context = self.get_context_data()
        usersocials = context['usersocials']
        with transaction.atomic():
            self.object = form.save()

            if usersocials.is_valid():
                usersocials.instance = self.object
                usersocials.save()

        tc_lib.generate_project_matches(form)

        return super(ProfileSocialUpdate, self).form_valid(form)


class ProfileView(generic.DetailView):
    """
    Profile Page View
    """
    model = User
    slug_field = "username"
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        """
        Puts User Matches in view, in order by rank (# of matching skills)
        :param kwargs:
        :return:
        """
        context = super(ProfileView, self).get_context_data(**kwargs)
        # only load if self.request.user == profile user id
        if self.request.user.id is self.object.id:
            context['match_list'] = Match.objects.filter(user=self.object.id).order_by('-rank')
        return context


class DashboardView(generic.ListView):
    """
    Dashboard Page View
    """
    template_name = 'accounts/dashboard.html'
    context_object_name = 'project_list'
    model = Project

    def get_context_data(self, **kwargs):
        """
        Puts Collab Request objects in context to list on dashboard.
        :param kwargs:
        :return:
        """
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'request_list': Request.objects.filter(recipient=self.request.user),
        })
        return context

    def get_queryset(self):
        """
        Puts Project objects in context to list on dashboard.
        :return:
        """
        return Project.objects.filter(founder=self.request.user)


def sendrequest(request, project_id):
    """
    When user requests to work on a project with another user, a Collab Request is created that will
    eventually be displayed on the recipient's dashboard the next time they log in.
    :param request: request.POST includes recipient id
    :param project_id: project id
    :return: redirects to dashboard
    """
    project = get_object_or_404(Project, pk=project_id)
    try:
        recipient = get_object_or_404(User, pk=request.POST['recipient_id'])

    except (KeyError, Match.DoesNotExist):
        return render(request, 'accounts/dashboard.html', {
            'project': project,
            'error_message': "You did not select a valid recipient",
        })
    else:
        sender = request.user
        req = Request(project=project, sender=sender, recipient=recipient, message="Let's work together")
        req.save()
        return redirect('accounts:dashboard')


def logout_view(request):
    """
    Logs the user out and redirects to the home page.
    :param request: logout request
    :return: redirects home
    """
    logout(request)
    return redirect('home')


class LoginView(View):
    """
    Login logic
    """
    form_class = UserLoginForm
    template_name = 'accounts/form.html'

    def get(self, request):
        """
        Displays login form.
        :param request: login request
        :return: login form
        """
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Validates login form data, authenticates user, logs user in, & redirects to dashboard.
        If login issue, goes back to login form.
        :param request:
        :return:
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            print(request.user.is_authenticated), 'yippy'
            return redirect('accounts:dashboard')
        return render(request, self.template_name, {'form': form})


class RegisterView(View):
    form_class = UserRegForm
    template_name = 'accounts/registration_form.html'

    def get(self, request):
        """
        Displays registration form.
        :param request: registration request
        :return: registration form
        """
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Validates form data, creates user, authenticates user, logs in user, & redirects to dashboard.
        :param request:
        :return:
        """
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
