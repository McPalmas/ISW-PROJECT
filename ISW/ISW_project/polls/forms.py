from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    User._meta.get_field('email')._unique = True

    class Meta:
        model = User
        fields = ('username',  'email', 'password1', 'password2', )