from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=156, null=False, blank=False, verbose_name='Title')

    body = models.TextField(max_length=2048, null=False, blank=False, verbose_name='Body')

    # perhaps should change on_delete param
    user = models.ForeignKey('authorization.User', on_delete=models.CASCADE, null=False, blank=False, verbose_name='User')

    # date when this post was created
    created_at = models.DateField(auto_now_add=True, verbose_name='Publication date')

    # theme field (mb should rename to topics)
    # theme = models.ManyToManyField(to='Theme')

    is_closed = models.BooleanField(default=False, verbose_name='Is problem solved?')

    # options: request or question
    REQUEST = 'REQUEST'
    QUESTION = 'QUESTION'
    PROBLEM_TYPE_OPTIONS = [
        (REQUEST, 'Request'),
        (QUESTION, 'Question'),
    ]
    problem_type = models.CharField(max_length=8,
                                    choices=PROBLEM_TYPE_OPTIONS,
                                    default=None, verbose_name='Problem type')

    # False for requests
    is_anonymous = models.BooleanField(default=False, verbose_name='Is problem anonymous?')
