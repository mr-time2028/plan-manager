from rest_framework import serializers

from users.serializers import UserSerialzier
from .group_serializers import GroupSerializer
from ..models import Board


class BoardSerializer(serializers.ModelSerializer):
    group_set = GroupSerializer(many=True, required=False, read_only=True)
    members = UserSerialzier(many=True, required=False, read_only=True)

    class Meta:
        model = Board
        fields = ("title", "slug", "group_set", "members")
