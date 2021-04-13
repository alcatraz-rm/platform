from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import *


@login_required
def add_problem_view(request):
    if request.method == 'POST':
        form = NewProblemForm(data=request.POST)

        if form.is_valid():
            new_problem = form.save(commit=False)

            new_problem.user = request.user

            new_problem.save()

            form.save_m2m()

            return redirect(new_problem.get_absolute_url())
    else:
        form = NewProblemForm(data=request.GET)

        return render(request, 'questions/add_problem.html', {'form': form})
