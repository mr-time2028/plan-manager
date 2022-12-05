from rest_framework import serializers

from workspaces.models import Group
from .task_serializer import TaskSerializer


class GroupSerializer(serializers.ModelSerializer):
    task_set = TaskSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = "__all__"
