from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.serializers import UserSerialzier
from .board_serializers import BoardSerializer
from workspaces.models import (
    Workspace,
    Board,
)


class WorkspaceCreateSerializer(serializers.ModelSerializer):
    board = serializers.SlugRelatedField(
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
        fields = ("title", "slug", "board", "members")


class WorkspaceUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fields = ("title", "slug")


class WorkspaceSerializer(serializers.ModelSerializer):
    board = BoardSerializer(many=True, required=False, read_only=True)
    members = serializers.SerializerMethodField("get_members")
    owners = serializers.SerializerMethodField("get_owners")

    class Meta:
        model = Workspace
        fields = ("id", "title", "slug", "board", "owners", "members")

    def get_owners(self, obj):
        owners = obj.members.filter(workspace_user__role='o')
        serializer = UserSerialzier(owners, many=True)
        return serializer.data

    def get_members(self, obj):
        members = obj.members.filter(workspace_user__role='m')
        serializer = UserSerialzier(members, many=True)
        return serializer.data


class WorkspaceUserSerialzier(serializers.Serializer):
    members = serializers.DictField()
