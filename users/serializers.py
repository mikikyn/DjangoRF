from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    code = serializers.CharField(max_length=6)

    def ConfirmValidate(self, data):
        username = data.get('username')
        code = data.get('code')
        try:
            user = User.objects.get(username=username)
            confirmation = user.confirmation_code
            if not confirmation or confirmation.code != code:
                raise ValidationError('Invalid confirmation code.')
        except User.DoesNotExist:
            raise ValidationError('User does not exist.')

        return data