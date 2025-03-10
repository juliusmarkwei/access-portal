from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from djoser.views import UserViewSet
from .serializers import CustomTokenObtainPairSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


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
        summary="Log in user based on email and password",
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


@extend_schema(tags=["Auth"])
class CustomTokenRefreshView(TokenRefreshView):
    """Token refresh view"""

    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pass


@extend_schema(tags=["Auth"])
class CustomUserViewSet(UserViewSet):
    """Custom implementation of user view set."""

    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pass
