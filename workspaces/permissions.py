from rest_framework import permissions

from .models import WorkspaceUser


class IsPartOf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsWorkspaceOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            workspace_user = WorkspaceUser.objects.get(workspace=obj, member=request.user)
            return workspace_user.role == 'o'
        except Exception:
            return False


class IsWorkspaceMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            workspace_user = WorkspaceUser.objects.get(workspace=obj, member=request.user)
            return workspace_user.role == 'm'
        except:
            return False


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
