from rest_framework import serializers

from users.serializers import UserSerialzier
from workspaces.models import Task


class TaskSerializer(serializers.ModelSerializer):
    users = UserSerialzier(many=True, required=False)

    class Meta:
        model = Task
        fields = "__all__"
