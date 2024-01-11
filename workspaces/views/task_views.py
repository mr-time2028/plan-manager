from rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from ..models import Task
from ..serializers.task_serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
)


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return TaskCreateSerializer
        elif self.action == "update":
            return TaskUpdateSerializer
        else:
            return TaskSerializer

    def list(self, request):
        serializer = self.get_serializer(instance=self.queryset, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data["title"]

            if Task.objects.filter(title=title).exists():
                return Response({
                    "error": True,
                    "detail": "there is a task with this title already."
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({"success": "Task created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(instance=task, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(instance=task, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        task = self.get_object()
        task.delete()
        return Response({"success": "Task deleted successfully."}, status=status.HTTP_200_OK)
