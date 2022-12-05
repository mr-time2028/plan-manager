from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.serializers import UserSerialzier
from .board_serializers import BoardSerializer
from workspaces.models import (
    Workspace,
    Board,
)


class WorkspaceCreateSerializer(serializers.ModelSerializer):
    board_set = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field="title",
        queryset=Board.objects.all()
    )
    members = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field="username",
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Workspace
        fields = ("title", "slug", "board_set", "members")


class WorkspaceUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fields = ("title", "slug")


class WorkspaceSerializer(serializers.ModelSerializer):
    board_set = BoardSerializer(many=True, required=False, read_only=True)
    members = UserSerialzier(many=True, required=False, read_only=True)

    class Meta:
        model = Workspace
        fields = ("id", "title", "slug", "board_set", "members")


class WorkspaceUserSerialzier(serializers.Serializer):
    members = serializers.DictField()
