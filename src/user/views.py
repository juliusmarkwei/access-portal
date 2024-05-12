from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AdminUserViewSerializer, CustomTokenObtainPairSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from api.paginator import QueryResultPagination


class ListSchoolInfoView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pagination_class = QueryResultPagination

    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_active=True)

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        # paginating results if more than 10
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(users, request)

        serializer = AdminUserViewSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "email": {},
                    "password": {},
                },
                "required": ["email", "password"],
            }
        },
        responses=CustomTokenObtainPairSerializer,
        tags=["Auth"],
        summary="Log in user based on email and password and whether account is active  or deactivated",
        description="This endpoint checks if the user account is activated or deactivated",
    )
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data.get("email"))
            if not user.is_active:
                return Response(
                    {"detail": "Account not activated"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except User.DoesNotExist:
            return Response(
                {"error": "Wrong credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().post(request, *args, **kwargs)
