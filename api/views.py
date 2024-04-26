from django.contrib.auth import get_user_model
from src.key.models import AccessKey
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import *
from .utils import generateAccessKey, sendEmail
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


# School's IP personne; API Views
class ITPersonalAccessKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        keyTag = request.query_params.get("key-tag", None)
        if keyTag:
            try:
                key = AccessKey.objects.get(owner=user, key_tag=keyTag)
            except AccessKey.DoesNotExist:
                return Response(
                    {"error": f"Key ({keyTag}) not found!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = AccessKeySerializer(key)
            return Response(serializer.data, status=status.HTTP_200_OK)
        keys = AccessKey.objects.filter(owner=user)
        serializer = AccessKeySerializer(keys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        key_tag = request.data.get("key-tag", None)
        validity_duration_days = request.data.get("validity-duration-days", None)
        validity_duration_months = request.data.get("validity-duration-months", None)
        if not key_tag:
            return Response(
                {"error": "Key-tag is required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        activeKeyExist = AccessKey.objects.filter(owner=user, status="active").exists()
        if activeKeyExist:
            return Response(
                {"error": "You already have an active key!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        inactveKeyExist = AccessKey.objects.filter(
            owner=user, status="inactive"
        ).exists()
        if inactveKeyExist:
            return Response(
                {"error": "You already have an inactive key pending to be activated!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not validity_duration_days and not validity_duration_months:
            return Response(
                {
                    "error": "'validity-duration-days' or 'validity-duration-months' is required!"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if validity_duration_days:
            calculated_validity_duration_days = int(validity_duration_days)
            if calculated_validity_duration_days < 1:
                return Response(
                    {
                        "error": "Validity duration must be greater than 0 and less than 365 days!"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif validity_duration_months:
            calculated_validity_duration_days = int(validity_duration_months) * 30

            if calculated_validity_duration_days < 1:
                return Response(
                    {
                        "error": "Validity duration must be greater than 0 and less than 12 months!"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        print("calculated_validity_duration_days", calculated_validity_duration_days)
        if calculated_validity_duration_days > 365:
            return Response(
                {"error": "Validity duration must be less than 365 days!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "key": generateAccessKey(),
            "key_tag": key_tag,
            "owner": user.id,
            "status": "inactive",
            "validity_duration_days": calculated_validity_duration_days,
        }
        serializer = AccessKeySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin API View
class AdminAccessKeyActivationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        userEmail = request.data.get("email", None)
        userKeytag = request.data.get("key-tag", None)
        if not userEmail and not userKeytag:
            return Response(
                {"error": "Email and key-tag are required to activate a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not userEmail:
            return Response(
                {"error": "Email is required to activate a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not userKeytag:
            return Response(
                {"error": "Key-tag is required to activate a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=userEmail)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            key = AccessKey.objects.get(
                owner=user, status="inactive", key_tag=userKeytag
            )
        except AccessKey.DoesNotExist:
            return Response(
                {"error": f"No inactive key ({userKeytag}) found for this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        key.status = "active"

        # Set key expiry date to 30 days from now
        activation_date = timezone.now()
        expiry_date = activation_date + timedelta(days=key.validity_duration_days)

        key.procurement_date = activation_date
        key.expiry_date = expiry_date
        key.save()

        expiry_date_formatted = expiry_date.strftime("%d %B, %Y %H:%M %p")
        data = {
            "key": key.key,
            "expiry_date": expiry_date_formatted,
            "owner": user.full_name,
            "validity_days": key.validity_duration_days,
        }
        sendEmail(accessGranted=True, recipient=user.email, keyData=data)
        return Response(
            {"message": "Key activated successfully"},
            status=status.HTTP_200_OK,
        )


class AdminAccessKeyRevocationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        userEmail = request.data.get("email", None)
        userKeyTag = request.data.get("key-tag", None)
        if not userEmail and not userKeyTag:
            return Response(
                {"error": "Email and key-tag are required to revoke a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not userEmail:
            return Response(
                {"error": "Email is required to revoke a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not userKeyTag:
            return Response(
                {"error": "Key-tag is required to revoke a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=userEmail)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            key = AccessKey.objects.get(owner=user, status="active", key_tag=userKeyTag)
        except AccessKey.DoesNotExist:
            return Response(
                {"error": f"No active key ({userKeyTag}) found for this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        key.status = "revoked"
        key.save()

        data = {
            "owner": user.full_name,
        }
        sendEmail(KeyRevoked=True, recipient=user.email, keyData=data)
        return Response(
            {"message": "Key revoked successfully"},
            status=status.HTTP_200_OK,
        )


class AdminAccessKeyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        keys = AccessKey.objects.all()
        serializer = AdminAccessKeySerializer(keys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
