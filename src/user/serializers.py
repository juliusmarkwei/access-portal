from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime

User = get_user_model()


class UserCreateSerializer(BaseUserCreatePasswordRetypeSerializer):
    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ("email", "full_name", "phone", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def perform_create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        message = "Check your email to verify your account."
        return {"data": data, "status": "success", "message": message}


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("email", "full_name", "phone", "is_active", "is_admin")
        extra_kwargs = {"password": {"write_only": True}}


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # remove is_admin and is_active from serializer

    def validate(self, attrs):
        data = super().validate(attrs)
        obj = self.user
        data.update(
            {
                "is_admin": obj.is_admin,
            }
        )
        return data
