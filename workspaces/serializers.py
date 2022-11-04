from rest_framework import serializers

from .models import (
    Group,
    Workspace,
    Board,
    Task,
)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    task_set = TaskSerializer(many=True)

    class Meta:
        model = Group
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    group_set = GroupSerializer(many=True)

    class Meta:
        model = Board
        fields = "__all__"


class WorkspaceSerializer(serializers.ModelSerializer):
    board_set = BoardSerializer(many=True)

    class Meta:
        model = Workspace
        fields = "__all__"
