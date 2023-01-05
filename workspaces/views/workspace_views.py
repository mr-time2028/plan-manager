from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import (
    Workspace,
    WorkspaceUser,
)
from ..serializers.workspace_serializers import (
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
    """ 
    TODO: an ability that allow owner to change role of other members
    """
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    lookup_field = "slug"

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ["update", "destroy", "add_member", "remove_member"]:
            self.permission_classes.append(IsWorkspaceOwner | IsSuperuser)
        elif self.action in ["retrieve"]:
            self.permission_classes.append(IsPartOf | IsSuperuser)
        elif self.action in ["all_workspaces"]:
            self.permission_classes.append(IsSuperuser)

        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return WorkspaceCreateSerializer
        elif self.action == "update":
            return WorkspaceUpdateSerializer
        elif self.action in ["add_member", "remove_member"]:
            return WorkspaceUserSerialzier
        else:
            return WorkspaceSerializer

    def list(self, request):
        raise MethodNotAllowed("get", code=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=["get"])
    def user_workspaces(self, request):
        user_workspaces = self.queryset.filter(members=request.user)
        serializer = self.get_serializer(instance=user_workspaces, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def all_workspaces(self, request):
        serializer = self.get_serializer(instance=self.queryset, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        TODO: allow workspace creators to determine role of members (owner or member) when add them
        """
        # remove owner username if owner enter own username in the members list
        members = request.data.get("members")
        if members:
            members = list(set(members))
            owner_username = request.user.username
            if owner_username in members:   
                members.remove(owner_username)
            request.data["members"] = members

        serializer = self.get_serializer(data=request.data, context={"request": request})
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
        serializer = self.get_serializer(instance=workspace, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug=None):
        workspace = self.get_object()
        serializer = self.get_serializer(instance=workspace, data=request.data, partial=True)
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
        serializer = self.get_serializer(data=request.data)
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
                    role=WorkspaceUser.OWNER if role == "owner" else WorkspaceUser.MEMBER,
                ) for member, role in zip(members_objs, roles)
            ]
            WorkspaceUser.objects.bulk_create(workspace_user_objs, ignore_conflicts=True)   
            return Response({"success": "The received members were added to the received workspace."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def remove_member(self, request, slug=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            members = serializer.data["members"].keys()

            workspace = self.get_object()
            WorkspaceUser.objects.filter(workspace=workspace, member__username__in=members).delete()
            return Response({"success": "The received members were removed from the received workspace."}, status=status.HTTP_200_OK)
