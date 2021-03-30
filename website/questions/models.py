from django.conf import settings
from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=156, null=False, blank=False, verbose_name='Title', )

    body = models.TextField(max_length=2048, null=False, blank=False, verbose_name='Body', )

    # perhaps should change on_delete param
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, null=True, blank=False,
                             verbose_name='User', default=None, )

    # date when this post was created
    created_at = models.DateField(auto_now_add=True, verbose_name='Publication date', )

    topics = models.ManyToManyField(to='Section', verbose_name='Topics', related_name='topics', )

    is_closed = models.BooleanField(default=False, verbose_name='Is problem solved?', )

    problem_type = models.CharField(max_length=8,
                                    choices=settings.PROBLEM_TYPE_OPTIONS,
                                    default=None, verbose_name='Problem type', )

    # False for requests
    is_anonymous = models.BooleanField(default=False, verbose_name='Is problem anonymous?', )


class Response(models.Model):
    # perhaps should change on_delete param
    problem = models.ForeignKey(Problem, on_delete=models.SET_DEFAULT, null=False, blank=False,
                                verbose_name='Problem', default=None, )

    body = models.TextField(max_length=2048, null=False, blank=False, verbose_name='Body', )

    # perhaps should change on_delete param
    author = models.ForeignKey('authorization.User', on_delete=models.SET_DEFAULT, null=False, blank=False,
                             verbose_name='Author', default=None, )

    # date when the response was created
    created_at = models.DateField(auto_now_add=True, verbose_name='Publication date', )

    anonymous = models.BooleanField()

    # this action makes question resolved
    final = models.BooleanField()


class Science(models.Model):
    # TODO: add sciences
    name = models.CharField(verbose_name='Science name', null=False, blank=False, choices=(('science_1', 'science_1'),
                                                                                           ('science_2', 'science_2')),
                            max_length=64, )


class Subject(models.Model):
    # TODO: add subjects
    science = models.ForeignKey(to='Science', on_delete=models.CASCADE, null=False, blank=False, )

    name = models.CharField(verbose_name='Subject name', null=False, blank=False, choices=(('sub_1', 'sub_1'),
                                                                                           ('sub_2', 'sub_2')),
                            max_length=64, )


class Section(models.Model):
    # TODO: add sections
    subject = models.ForeignKey(to='Subject', on_delete=models.CASCADE, null=False, blank=False, )

    name = models.CharField(verbose_name='Section name', null=False, blank=False, choices=(('section_1', 'section_1'),
                                                                                           ('section_2', 'section_2')),
                            max_length=64, )
