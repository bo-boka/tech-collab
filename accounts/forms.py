from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from .models import UserProfile
from django import forms


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("This user does not exist.")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password.")
        if not user.is_active:
            raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


# class UserProfileForm(forms.ModelForm):
#
#     class Meta:
#         model = UserProfile
#         fields = ['phone', 'city']
