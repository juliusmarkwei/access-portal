from django.contrib.auth import get_user_model
from rest_framework import serializers
from src.key.models import AccessKey

User = get_user_model()


class AccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        fields = "__all__"

    def create(self, validated_data):
        key = AccessKey.objects.create(**validated_data)
        return key

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("owner")
        data.pop("created_at")
        data.pop("id")
        return data
