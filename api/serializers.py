from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("email", "full_name", "phone", "is_admin")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        message = "Welcome to Access Portal! Check your email to verify your account."
        validated_data["message"] = message
        return validated_data


class UserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ("email", "full_name", "phone_number", "is_active", "is_admin")
        extra_kwargs = {"password": {"write_only": True}}
