from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['email', 'login', 'first_name', 'last_name', 'phone_number', 'is_verified', 'is_staff', 'is_active']
    list_filter = ['is_verified', 'is_staff', 'is_active']
    search_fields = ['email', 'login', 'first_name', 'last_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'login', 'phone_number')}),
        ('Permissions', {'fields': ('is_verified', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'login', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_verified', 'is_staff', 'is_active'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')
