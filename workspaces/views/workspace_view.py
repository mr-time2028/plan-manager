from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import (
    Workspace,
    WorkspaceUser,
)
from ..serializers.workspace_serializer import (
    WorkspaceSerializer,
    WorkspaceCreateSerializer,
    WorkspaceUpdateSerializer,
    WorkspaceUserSerialzier,
)
from ..permissions import (
    IsPartOf,
    IsWorkspaceOwner,
    IsSuperuser,
)


class WorkspaceView(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    lookup_field = "slug"

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ["create", "update", "destroy", "add_member", "remove_member"]:
            self.permission_classes.append(IsWorkspaceOwner | IsSuperuser)
        if self.action in ["retrieve"]:
            self.permission_classes.append(IsPartOf | IsSuperuser)
        if self.action == "all_workspaces":
            self.permission_classes.append(IsSuperuser)

        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=["get"])
    def user_workspaces(self, request):
        user_workspaces = self.queryset.filter(members=request.user)
        serializer = WorkspaceSerializer(instance=user_workspaces, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def all_workspaces(self, request):
        serializer = WorkspaceSerializer(instance=self.queryset, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        # remove owner username if owner enter own username in the members list
        members = request.data.get("members", None)
        if members:
            members = list(set(members))
            owner_username = request.user.username
            if owner_username in members:
                members.remove(owner_username)
            request.data["members"] = members

        serializer = WorkspaceCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data["title"]

            # check if the owner has a duplicate title
            if Workspace.objects.filter(Q(title=title) & Q(members=request.user)).exists():
                return Response({"detail": "User already has a workspace with this title."}, status=status.HTTP_400_BAD_REQUEST)

            workspace = serializer.save()
            WorkspaceUser.objects.create(workspace=workspace, member=request.user, role="o")

            return Response({"success": "Workspace created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, slug=None):
        workspace = self.get_object()
        serializer = WorkspaceSerializer(instance=workspace, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug=None):
        workspace = self.get_object()
        serializer = WorkspaceUpdateSerializer(instance=workspace, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug=None):
        workspace = self.get_object()
        workspace.delete()
        return Response({"success": "Workspace deleted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def add_member(self, request, slug=None):
        serializer = WorkspaceUserSerialzier(data=request.data)
        if serializer.is_valid(raise_exception=True):
            members_roles = serializer.data["members"]

            members = members_roles.keys()
            roles = members_roles.values()

            # validation received roles with model roles
            model_roles = [role_tuple[1] for role_tuple in WorkspaceUser.ROLE_CHOICES]
            if not all(role in model_roles for role in list(set(roles))):
                return Response({"detail": "The wrong type was received for the user."}, status=status.HTTP_400_BAD_REQUEST)

            workspace = self.get_object()
            members_objs = list(get_user_model().objects.in_bulk(members, field_name="username").values())
            workspace_user_objs = [
                WorkspaceUser(
                    workspace=workspace,
                    member=member,
                    role='o' if role == "owner" else 'm',
                ) for member, role in zip(members_objs, roles)
            ]
            WorkspaceUser.objects.bulk_create(workspace_user_objs, ignore_conflicts=True)   
            return Response({"success": "The received members were added to the received workspace."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def remove_member(self, request, slug=None):
        serializer = WorkspaceUserSerialzier(data=request.data)
        if serializer.is_valid(raise_exception=True):
            members = serializer.data["members"]

            workspace = self.get_object()
            WorkspaceUser.objects.filter(workspace=workspace, member__username__in=members).delete()
            return Response({"success": "The received members were removed from the received workspace."}, status=status.HTTP_200_OK)
