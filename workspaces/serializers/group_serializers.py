from rest_framework import serializers

from workspaces.models import (
    Group,
    Board,
)
from .task_serializers import TaskSerializer


class GroupCreateSerializer(serializers.ModelSerializer):
    board = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Board.objects.all(),
    )

    class Meta:
        model = Group
        fields = ("title", "board")


class GroupSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = ("id", "title", "board", "task")


class GroupUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ("title",)
