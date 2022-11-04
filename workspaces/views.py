from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Workspace
from .serializers import WorkspaceSerializer


class WorkspaceView(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def all_workspaces(self, request):
        workspaces = Workspace.objects.filter(members=self.request.user)
        serializer = WorkspaceSerializer(instance=workspaces, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
