from django.contrib.auth import get_user_model
from rest_framework import serializers
from src.key.models import AccessKey
from datetime import datetime

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


class AdminAccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["owner"] = instance.owner.email

        if data["expiry_date"]:
            formatted_expiry_date = datetime.strptime(
                data["expiry_date"].replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f"
            )
            data["expiry_date"] = formatted_expiry_date.strftime("%d %B, %Y %I:%M %p")

        if data["procurement_date"]:
            formatted_procurement_date = datetime.strptime(
                data["procurement_date"].replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f"
            )
            data["procurement_date"] = formatted_procurement_date.strftime(
                "%d %B, %Y %I:%M %p"
            )

        formatted_created_at = datetime.strptime(
            data["created_at"].replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f"
        )
        data["created_at"] = formatted_created_at.strftime("%d %B, %Y %I:%M %p")

        data.pop("id")
        return data


# Serializers for Spectaculr UI View
class AccessKeySerializerDocsView(AccessKeySerializer):
    class Meta(AccessKeySerializer.Meta):
        fields = [
            "key",
            "key_tag",
            "validity_duration_days",
            "status",
            "procurement_date",
            "expiry_date",
        ]


class AccessKeySerializerDocsPOST(AccessKeySerializer):
    class Meta(AccessKeySerializer.Meta):
        fields = [
            "key_tag",
            "validity_duration_days",
        ]


class AdminAccessKeySerializerDocsPOST(AccessKeySerializer):
    email = serializers.EmailField()

    class Meta(AccessKeySerializer.Meta):
        fields = [
            "email",
            "key_tag",
        ]


class AdminAccessKeySerializerDocsREVOKE(AccessKeySerializer):
    email = serializers.EmailField()

    class Meta(AccessKeySerializer.Meta):
        fields = [
            "email",
            "key_tag",
        ]
