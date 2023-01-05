from django.db.models import Q

from rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import Group
from ..serializers.group_serializers import (
    GroupSerializer,
    GroupCreateSerializer,
    GroupUpdateSerializer,
)
from ..permissions import (
    IsSuperuser,
    IsGroupOwner,
)


class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action in ["all_groups"]:
            self.permission_classes.append(IsSuperuser)
        elif self.action in ["create", "retrieve", "update", "destroy"]:
            self.permission_classes.append(IsGroupOwner | IsSuperuser)

        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return GroupCreateSerializer
        elif self.action == "update":
            return GroupUpdateSerializer
        else:
            return GroupSerializer

    def list(self, request):
        raise MethodNotAllowed("get", code=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=["get"])
    def all_groups(self, request):
        serializer = self.get_serializer(instance=self.queryset, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data["title"]
            board_slug = serializer.validated_data["board"]

            # check if the group has a duplicate title
            if Group.objects.filter(Q(title=title) & Q(board__slug=board_slug)).exists():
                return Response({"detail": "Board already has a group with this title."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({"success": "Group created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        group = self.get_object()
        serializer = self.get_serializer(instance=group, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        group = self.get_object()
        serializer = self.get_serializer(instance=group, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        group = self.get_object()
        group.delete()
        return Response({"success": "Group deleted successfully."}, status=status.HTTP_200_OK)
