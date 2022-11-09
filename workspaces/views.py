from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Workspace
from .serializers import WorkspaceSerializer


class WorkspaceView(viewsets.ViewSet):

    @action(detail=False, methods=['get'], permission_classes=(IsAuthenticated,))
    def user_workspaces(self, request):
        workspaces = Workspace.objects.filter(members=request.user)
        serializer = WorkspaceSerializer(instance=workspaces, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
