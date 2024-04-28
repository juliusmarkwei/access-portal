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
        if data["status"] != "active":
            data["key"] = data["key"][:10] + "..."

        if data["expiry_date"]:
            # Remove milliseconds if present
            expiry_date_string = data["expiry_date"].replace("Z", "").split(".")[0]
            formatted_expiry_date = datetime.strptime(
                expiry_date_string, "%Y-%m-%dT%H:%M:%S"
            )
            data["expiry_date"] = formatted_expiry_date.strftime("%d %B, %Y %I:%M %p")

        if data["procurement_date"]:
            # Remove milliseconds if present
            procurement_date_string = (
                data["procurement_date"].replace("Z", "").split(".")[0]
            )
            formatted_procurement_date = datetime.strptime(
                procurement_date_string, "%Y-%m-%dT%H:%M:%S"
            )
            data["procurement_date"] = formatted_procurement_date.strftime(
                "%d %B, %Y %I:%M %p"
            )

        return data


class AdminAccessKeySerializer(serializers.ModelSerializer):
    owner = serializers.EmailField()

    class Meta:
        model = AccessKey
        exclude = ("id",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["owner"] = instance.owner.email

        if data["expiry_date"]:
            # Remove milliseconds if present
            expiry_date_string = data["expiry_date"].replace("Z", "").split(".")[0]
            formatted_expiry_date = datetime.strptime(
                expiry_date_string, "%Y-%m-%dT%H:%M:%S"
            )
            data["expiry_date"] = formatted_expiry_date.strftime("%d %B, %Y %I:%M %p")

        if data["procurement_date"]:
            # Remove milliseconds if present
            procurement_date_string = (
                data["procurement_date"].replace("Z", "").split(".")[0]
            )
            formatted_procurement_date = datetime.strptime(
                procurement_date_string, "%Y-%m-%dT%H:%M:%S"
            )
            data["procurement_date"] = formatted_procurement_date.strftime(
                "%d %B, %Y %I:%M %p"
            )

        # Remove milliseconds if present
        created_at_string = data["created_at"].replace("Z", "").split(".")[0]
        formatted_created_at = datetime.strptime(created_at_string, "%Y-%m-%dT%H:%M:%S")
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


class AdminAccessKeySerializerDocsActionView(AccessKeySerializer):
    email = serializers.EmailField()

    class Meta(AccessKeySerializer.Meta):
        fields = [
            "email",
        ]
