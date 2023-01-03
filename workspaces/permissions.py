from django.db.models import Q

from rest_framework import permissions

from .models import (
    Workspace,
    WorkspaceUser,
)


class IsPartOf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsWorkspaceOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        workspace_slug = request.data.get("workspace")
        if workspace_slug:
            return Workspace.objects.filter(
                Q(slug=workspace_slug) & \
                Q(workspace_user__member=request.user) & \
                Q(workspace_user__role=WorkspaceUser.OWNER)
            ).exists()
        return True

    def has_object_permission(self, request, view, obj):
        try:
            workspace_user = WorkspaceUser.objects.get(workspace=obj, member=request.user)
            return workspace_user.role == WorkspaceUser.OWNER
        except Exception:
            return False


class IsBoardOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return Workspace.objects.filter(
            Q(slug=obj.workspace.slug) & \
            Q(workspace_user__member=request.user) & \
            Q(workspace_user__role=WorkspaceUser.OWNER)
        ).exists()


class IsWorkspaceMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            workspace_user = WorkspaceUser.objects.get(workspace=obj, member=request.user)
            return workspace_user.role == WorkspaceUser.MEMBER
        except:
            return False


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
