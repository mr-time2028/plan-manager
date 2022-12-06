from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..permissions import IsSuperuser
from workspaces.models import Board
from ..serializers.board_serializers import BoardSerializer


class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    lookup_field = "slug"

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action == "all_boards":
            self.permission_classes.append(IsSuperuser)

        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=["get"])
    def user_boards(self, request):
        user_boards = self.queryset.filter(members=request.user)
        serializer = BoardSerializer(instance=user_boards, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def all_boards(self, request):
        serializer = BoardSerializer(instance=self.queryset, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
