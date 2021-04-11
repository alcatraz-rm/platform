from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from questions.models import Problem, Response


def problem_list(request):
    object_list = Problem.objects.all()

    paginator = Paginator(object_list, 3)

    page_no = request.GET.get('page')

    try:

        posts = paginator.page(page_no)
    except PageNotAnInteger:
        # if page_no is no an integer show the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_no is out of bounds, then show last available page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'feed/list.html', {'posts': posts, 'page_no': page_no})


class ProblemListView(ListView):

    queryset = Problem.objects.all()

    context_object_name = 'posts'

    paginate_by = 3

    template_name = 'feed/list.html'


def problem_detail(request, post_id):

    post = get_object_or_404(Problem, id=post_id)

    responses = post.comments.all()

    return render(request, 'feed/detail.html', {'post': post, 'responses': responses})
