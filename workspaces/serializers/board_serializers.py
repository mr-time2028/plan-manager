from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.serializers import UserSerialzier
from .group_serializers import GroupSerializer
from ..models import (
    Board,
    Task,
    Workspace,
)


class BoardSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=True, required=False, read_only=True)
    members = UserSerialzier(many=True, required=False, read_only=True)

    class Meta:
        model = Board
        fields = ("id", "title", "slug", "group", "members")


class BoardCreateSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field="pk",
        queryset=Task.objects.all()
    )
    members = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field="username",
        queryset=get_user_model().objects.all()
    )
    workspace = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Workspace.objects.all(),
    )

    class Meta:
        model = Workspace
        fields = ("title", "workspace", "slug", "group", "members")


class BoardUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ("title", "slug")


class BoardUserSerialzier(serializers.Serializer):
    members = serializers.ListField()
