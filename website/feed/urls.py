from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ProblemListView.as_view(), name='problem_list'),
    url(r'^(?P<post_id>\d)', views.problem_detail, name='problem_detail'),
]