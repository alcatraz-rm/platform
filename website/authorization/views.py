from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import SingUpForm, LoginForm


def sing_up_view(request):
    if request.method == 'POST':
        user_form = SingUpForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password1'])
            # Save the User object
            new_user.save()

            return render(request, 'authorization/sing_up_success.html', {'new_user': new_user})
    else:
        user_form = SingUpForm()

    return render(request, 'authorization/singup.html', {'user_form': user_form})


def user_login_view(request):
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
                # else:
                #     return HttpResponse('Disabled account')
            # else:
            #     return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, template, {'form': form})
