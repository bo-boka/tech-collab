from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
# ^to overwrite the built-in admin user model to add properties


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['phone', 'city', 'state']
