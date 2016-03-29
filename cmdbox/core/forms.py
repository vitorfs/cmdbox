from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        help_text='Not required. The email address will only be used for password reset.',
        max_length=254,
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email')
