from django.contrib import admin

from workspaces.models import Task, Group, Workspace, Board, WorkspaceUser


class WorkspaceUserInline(admin.TabularInline):
    model = WorkspaceUser


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at']
    inlines = [WorkspaceUserInline]


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'board']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'expire_at', 'created_at', 'updated_at']
