from django.contrib import admin

from workspaces.models import (
    Task,
)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'created_at', 'updated_at']
