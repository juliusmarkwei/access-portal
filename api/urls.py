from django.urls import path
from .views import *
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "access-portal-api"

urlpatterns = [
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/signup/", UserViewSet.as_view({"post": "create"}), name="signup"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path(
        "auth/activate/", UserViewSet.as_view({"post": "activation"}), name="activate"
    ),
    path(
        "auth/reset-password/",
        UserViewSet.as_view({"post": "reset_password"}),
        name="reset_password",
    ),
    path(
        "auth/reset-password-confirm/",
        UserViewSet.as_view({"post": "reset_password_confirm"}),
        name="reset_password_confirm",
    ),
]
