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
        "auth/user/activate/",
        UserViewSet.as_view({"post": "activation"}),
        name="activate",
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
    path("auth/users/me/", UserViewSet.as_view({"get": "me"}), name="me"),
    path("auth/users/", UserViewSet.as_view({"get": "list"}), name="users"),
    path("access-key", ITPersonalAccessKeyView.as_view(), name="access-key"),
    path(
        "access-key/activate",
        AdminAccessKeyActivationView.as_view(),
        name="admin-access-key-activate",
    ),
    path(
        "access-key/revoke",
        AdminAccessKeyRevocationView.as_view(),
        name="admin-access-key-revoke",
    ),
]
