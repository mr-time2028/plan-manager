from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import permissions

from .models import (
    Workspace,
    WorkspaceUser,
    Board,
    Group,
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


class IsGroupOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        board_slug = request.data.get("board")
        try:
            board = get_object_or_404(Board, slug=board_slug)
            workspace = board.workspace
            return Workspace.objects.filter(
                Q(slug=workspace.slug) & \
                Q(workspace_user__member=request.user) & \
                Q(workspace_user__role=WorkspaceUser.OWNER)
            ).exists()
        except:
            return True

    def has_object_permission(self, request, view, obj):
        return Workspace.objects.filter(
            Q(slug=obj.board.workspace.slug) & \
            Q(workspace_user__member=request.user) & \
            Q(workspace_user__role=WorkspaceUser.OWNER)
        ).exists()


class IsTaskOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        group_id = request.data.get("group")

        try:
            group = get_object_or_404(Group, pk=group_id)
            workspace = group.board.workspace
            return Workspace.objects.filter(
                Q(slug=workspace.slug) & \
                Q(workspace_user__member=request.user) & \
                Q(workspace_user__role=WorkspaceUser.OWNER)
            ).exists()
        except:
            return True

    def has_object_permission(self, request, view, obj):
        return Workspace.objects.filter(
            Q(slug=obj.group.board.workspace.slug) & \
            Q(workspace_user__member=request.user) & \
            Q(workspace_user__role=WorkspaceUser.OWNER)
        ).exists()


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
