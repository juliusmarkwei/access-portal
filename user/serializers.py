from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer,
)

User = get_user_model()


class UserCreateSerializer(BaseUserCreatePasswordRetypeSerializer):
    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ("email", "full_name", "phone", "is_active", "is_admin", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def perform_create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        message = "Welcome to Access Portal! Check your email to verify your account."
        return {"data": data, "status": "success", "message": message}


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("email", "full_name", "phone", "is_active", "is_admin")
        extra_kwargs = {"password": {"write_only": True}}
