from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..permissions import (
    IsBoardOwner,
    IsSuperuser,
    IsPartOf,
)
from workspaces.models import (
    BoardUser,
    Workspace,
    Board,
    WorkspaceUser,
)
from ..serializers.board_serializers import (
    BoardSerializer,
    BoardCreateSerializer,
    BoardUpdateSerializer,
    BoardUserSerialzier,
)


class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = "slug"

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ["create", "update", "destroy", "add_member", "remove_member"]:
            self.permission_classes.append(IsBoardOwner | IsSuperuser)
        if self.action in ["retrieve"]:
            self.permission_classes.append(IsPartOf | IsSuperuser)
        if self.action in ["all_boards"]:
            self.permission_classes.append(IsSuperuser)

        return [permission() for permission in self.permission_classes]
    
    def get_serializer_class(self):
        if self.action == "create":
            return BoardCreateSerializer
        elif self.action == "update":
            return BoardUpdateSerializer
        elif self.action in ["add_member", "remove_member"]:
            return BoardUserSerialzier
        else:
            return BoardSerializer

    def list(self, request):
        raise MethodNotAllowed("get", code=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=["get"])
    def user_boards(self, request):
        user_boards = self.queryset.filter(members=request.user)
        serializer = BoardSerializer(instance=user_boards, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def all_boards(self, request):
        serializer = BoardSerializer(instance=self.queryset, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        TODO: board users must be a subset of workspace users
        """
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.data['title']
            workspace_slug = serializer.data["workspace"]
            board_members = serializer.data.get("members")

            workspace_obj = get_object_or_404(Workspace, slug=workspace_slug)
            board_obj = Board.objects.create(title=title, workspace=workspace_obj)

            if board_members:
                board_members_objs = list(get_user_model().objects.in_bulk(board_members, field_name="username").values())

                workspace_user_objs = [WorkspaceUser(workspace=workspace_obj, member=member) for member in board_members_objs]
                WorkspaceUser.objects.bulk_create(workspace_user_objs, ignore_conflicts=True)

                board_user_objs = [BoardUser(board=board_obj, member=member) for member in board_members_objs]
                BoardUser.objects.bulk_create(board_user_objs, ignore_conflicts=True)

            return Response({"success": "Board created successfully."})

    def retrieve(self, request, slug=None):
        board = self.get_object()
        serializer = BoardSerializer(instance=board, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug=None):
        board = self.get_object()
        serializer = BoardUpdateSerializer(instance=board, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug=None):
        board = self.get_object()
        board.delete()
        return Response({"success": "Board deleted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def add_member(self, request, slug=None):
        """
        TODO: check new user is a subset of workspace users
        """
        serializer = BoardUserSerialzier(data=request.data)
        if serializer.is_valid(raise_exception=True):
            members = serializer.data['members']
            board = self.get_object()
            workspace = board.workspace 

            if members:
                members_objs = list(get_user_model().objects.in_bulk(members, field_name="username").values())

                workspace_user_objs = [WorkspaceUser(workspace=workspace, member=member) for member in members_objs]
                WorkspaceUser.objects.bulk_create(workspace_user_objs, ignore_conflicts=True)

                board_user_objs = [BoardUser(board=board, member=member) for member in members_objs]
                BoardUser.objects.bulk_create(board_user_objs, ignore_conflicts=True)

            return Response({"success": "The received members were added to the received board."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def remove_member(self, request, slug=None):
        serializer = BoardUserSerialzier(data=request.data)
        if serializer.is_valid(raise_exception=True):
            members = serializer.data["members"]

            board = self.get_object()
            BoardUser.objects.filter(board=board, member__username__in=members).delete()
            return Response({"success": "The received members were removed from the received board."}, status=status.HTTP_200_OK)
