from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from ..models import Task
from ..serializers.task_serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
)
from ..utils import custom_filter


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_fields = ["status"]

    def get_serializer_class(self):
        if self.action == "create":
            return TaskCreateSerializer
        elif self.action == "update":
            return TaskUpdateSerializer
        else:
            return TaskSerializer

    @action(detail=False, methods=['get'])
    def home(self, request):
        return render(request, "home.html")

    # TODO: filter based on status

    def list(self, request):
        filtered_queryset = custom_filter(request, self.queryset, self.filter_fields)

        serializer = self.get_serializer(instance=filtered_queryset, context={"request": request}, many=True)
        return Response({
            "error": False,
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def create(self, request):
        create_serializer = TaskCreateSerializer(data=request.data, context={"request": request})
        if create_serializer.is_valid(raise_exception=True):
            # we can handle title uniqu later...
            task_instance = create_serializer.save()
            list_serializer = TaskSerializer(instance=task_instance, context={"request": request})    
            return Response({
                "error": False,
                "data": list_serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            "error": True,
            "data": create_serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

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
