from django.contrib.auth import get_user_model
from key.models import AccessKey
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import AccessKeySerializer
from .utils import generateAccessKey, sendEmail
from datetime import datetime, timedelta

User = get_user_model()


# School's IP personne; API Views
class ITPersonalAccessKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        keys = AccessKey.objects.filter(owner=user)
        serializer = AccessKeySerializer(keys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
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
        data = {"key": generateAccessKey(), "owner": user.id, "status": "inactive"}
        serializer = AccessKeySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            sendEmail(accessGranted=True, recipient=user.email, keyData=data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin API View
class AdminAccessKeyActivationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        userEmail = request.data.get("email", None)
        if userEmail:
            user = User.objects.get(email=userEmail)
            key = AccessKey.objects.filter(owner=user, status="inactive").first()
            if key:
                key.status = "active"

                # Set key expiry date to 30 days from now
                activation_date = datetime.now()
                expiry_date = activation_date + timedelta(days=30)

                key.procurement_date = activation_date
                key.expiry_date = expiry_date
                key.save()

                expiry_date_formatted = expiry_date.strftime("%d %B, %Y %H:%M %p")
                data = {
                    "key": key.key,
                    "expiry_date": expiry_date_formatted,
                    "owner": user.full_name,
                }
                sendEmail(accessGranted=True, recipient=user.email, keyData=data)
                return Response(
                    {"message": "Key activated successfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "No inactive key found for this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"error": "Email is required to activate a key."},
            status=status.HTTP_400_BAD_REQUEST,
        )
