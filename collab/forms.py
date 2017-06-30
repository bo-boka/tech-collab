from django.contrib.auth.models import User
from django import forms
# ^to overwrite the built-in admin user model to add properties


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
