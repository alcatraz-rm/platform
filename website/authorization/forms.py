from django import forms

from django.contrib.auth.forms import UserCreationForm

from authorization.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SingUpForm(UserCreationForm):
    email = forms.EmailField(max_length=64, help_text='Your email')

    name = forms.CharField(max_length=64, help_text='Your name')

    telegram = forms.CharField(max_length=32, help_text='Your telegram @nickname')

    vk = forms.URLField(max_length=256, help_text='Your VK-page url')

    class Meta:
        model = User

        fields = ('username', 'email', 'name', 'password1', 'password2', 'vk', 'telegram')
