from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.serializers import UserSerialzier
from workspaces.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "status", "description")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "status", "created_at", "updated_at")


class TaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("title", "status")
