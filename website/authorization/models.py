from django.db import models


# read about djago user model overriding
class User(models.Model):
    email = models.EmailField(max_length=64, null=False, blank=False, verbose_name="Email", )

    # warning
    password = models.CharField(max_length=64, null=False, blank=False, verbose_name="Password (warning)", )

    name = models.CharField(max_length=64, null=False, blank=False, verbose_name="Name", )

    phone = models.CharField(max_length=16, null=True, blank=False, default=None, verbose_name="Mobile Phone", )

    recovery_email = models.EmailField(max_length=64, null=True, blank=False, default=None, verbose_name="Recovery Email", )

    # nickname
    telegram = models.CharField(max_length=32, null=True, blank=False, default=None, verbose_name="Telegram Nickname", )

    # page url
    vk = models.URLField(max_length=256, null=True, blank=False, default=None, verbose_name="URL to VK page", )

    bio = models.TextField(max_length=512, null=True, blank=False, default=None, verbose_name="Bio", )

    # interests = models.ManyToManyField(to="interests", )

    photo = models.ImageField(verbose_name="Photo", )

    # TODO: add departments
    # required in v1
    department = models.CharField(max_length=80, null=True, blank=False, default=None, choices=(('department 1', 'department_1'),
                                                                                                ('department_2', 'department_2'),), verbose_name="Department", )

    # required in v1
    stage = models.CharField(max_length=16, null=True, blank=False, default=None, choices=(('stage_1', 'stage_1'),
                                                                                           ('stage_2', 'stage_2'),), verbose_name="Stage", )

    # subscribed_quiestions = models.ManyToManyField(to="Question", )

    # liked_quiestions = models.ManyToManyField(to="Question", )

    # liked_responses = models.ManyToManyField(to="Response", )

