from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import User
from questions.models import Section
from questions.forms import CustomMMCF


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user_qs = User.objects.filter(username=username)

        if user_qs.count() == 0:
            raise forms.ValidationError("The user does not exist")
        else:
            if username and password:
                user = authenticate(username=username, password=password)

                if not user:
                    raise forms.ValidationError("Incorrect password")
                if not user.is_active:
                    raise forms.ValidationError("This user is no longer active")

        return super().clean()


class SingUpForm(UserCreationForm):
    class Meta:
        model = User

        fields = ('username', 'email', 'recovery_email',
                  'first_name', 'last_name', 'department', 'stage', 'bio',
                  'password1', 'password2', 'vk', 'telegram', 'interests')

    first_name = forms.CharField(max_length=150, help_text='Your name', required=False)

    last_name = forms.CharField(max_length=150, help_text='Your last name', required=False)

    telegram = forms.CharField(max_length=32, help_text='Your telegram @nickname', required=False)

    vk = forms.URLField(max_length=256, help_text='Your VK-page url', required=False)

    interests = CustomMMCF(queryset=Section.objects.all(),
                           widget=forms.CheckboxSelectMultiple,
                           required=True, help_text="Please, choose at least ONE."
                           )
