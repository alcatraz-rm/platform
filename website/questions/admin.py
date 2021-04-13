from django.contrib import admin

from .models import *


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Question body', {'fields': ('title', 'body')}),
        ('Detailed info', {'fields': ('user', 'problem_type', 'is_closed', 'is_anonymous')}),
        ('Topics', {'fields': ('topics',)}),
    )

    list_display = ['created_at', 'title', 'user', 'problem_type', 'is_closed', 'is_anonymous']

    filter_horizontal = ['topics']

    list_filter = ['created_at', 'problem_type', 'is_closed', 'is_anonymous']

    ordering = ['created_at', 'title']

    date_hierarchy = 'created_at'

    # raw_id_fields = ('user',)

    '''list_select_related = (
        'user',
    )'''


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name']

    fieldsets = (
        (None, {'fields': ('name', 'subject')}),
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'science', )

    fieldsets = (
        (None, {'fields': ('name', 'science', )}),
    )


@admin.register(Science)
class ScienceAdmin(admin.ModelAdmin):
    list_display = ['name']

    fieldsets = (

        (None, {'fields': ('name',)}),
    )


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Response body', {'fields': ('problem', 'author', 'body', 'anonymous', 'final')}),
    )

    list_display = ('author', 'problem', 'created_at', 'final', 'anonymous',)

    list_filter = ('created_at', 'final', 'anonymous')

    search_fields = ('author', 'body', 'problem')
