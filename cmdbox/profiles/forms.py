from django import forms
from django.contrib.auth.models import User

from cmdbox.profiles.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('url', 'location', 'company')
