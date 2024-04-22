from django.contrib.auth import get_user_model
from key.models import AccessKey
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import AccessKeySerializer
from .utils import generateAccessKey

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

        data = {"key": generateAccessKey(), "owner": user.id, "status": "inactive"}
        serializer = AccessKeySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
