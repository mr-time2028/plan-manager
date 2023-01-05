from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.serializers import UserSerialzier
from workspaces.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field="username",
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Task
        fields = ("title", "users", "group")


class TaskSerializer(serializers.ModelSerializer):
    users = UserSerialzier(many=True, required=False, read_only=True)

    class Meta:
        model = Task
        fields = ("id", "title", "users", "status", "expire_at", "created_at", "updated_at")


class TaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("title", "expire_at", "status")
