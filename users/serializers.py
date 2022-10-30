from django.core.validators import RegexValidator

from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


PASSWORD_REGEX = RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})')
USERNAME_REGEX = RegexValidator(r'^[\w][\w\d_]+$')


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, validators=[USERNAME_REGEX])
    password1 = serializers.CharField(max_length=30, validators=[PASSWORD_REGEX])
    password2 = serializers.CharField(max_length=30, validators=[PASSWORD_REGEX])

    def validate(self, attrs):
        password1 = attrs.get('password1', None)
        password2 = attrs.get('password2', None)

        if password1 != password2:
            raise ValidationError({"detail": "Your passwords didn't match."}, code=status.HTTP_400_BAD_REQUEST)

        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=30)
