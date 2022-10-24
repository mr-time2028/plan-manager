from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    readonly_fields = [
        'created_at',
        'updated_at',
        'last_login'
    ]
    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_superuser',
        'is_active'
    )
    list_filter = (
        'is_superuser',
        'is_active'
    )
    fieldsets = (
        ('Security information', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_staff')}),
        ('Important date', {'fields': ('created_at', 'updated_at', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('first_name', 'last_name')