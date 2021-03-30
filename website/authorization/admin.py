from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DJUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DJUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone', 'recovery_email', 'telegram',
                                      'vk', 'bio', 'department', 'stage')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'user_permissions')}),
        ('Interests', {'fields': ('interests',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ['email', 'name', 'phone', 'recovery_email',
                    'telegram', 'vk', 'bio', 'department', 'stage']

    filter_horizontal = ['interests']
