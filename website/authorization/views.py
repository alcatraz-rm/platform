from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import SingUpForm, LoginForm


@user_passes_test(lambda user_obj: not user_obj.is_authenticated,
                  login_url='/feed', redirect_field_name='')
def sing_up_view(request):
    """

    If user is authenticated he'll redirected to /feed page, otherwise he'll get the sing-up form.

    """
    if request.method == 'POST':
        user_form = SingUpForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            user_form.save_m2m()

            # logging in a new user automatically
            data = user_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password1'])

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect(to='/feed/')
            # return render(request, 'authorization/sing_up_success.html', {'new_user': new_user})
    else:
        user_form = SingUpForm()

    return render(request, 'authorization/singup.html', {'user_form': user_form})


@user_passes_test(lambda user_obj: not user_obj.is_authenticated,
                  login_url='/feed', redirect_field_name='')
def user_login_view(request):
    """

    If user is authenticated he'll redirected to /feed page, otherwise he'll get the log-in form.

    """
    template = 'authorization/login.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = authenticate(username=data['username'], password=data['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect(to='/feed/')
    else:
        form = LoginForm()

    return render(request, template, {'form': form})


def user_logout_view(request):
    logout(request)

    return redirect(to=settings.LOGIN_URL)
