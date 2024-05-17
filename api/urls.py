from django.urls import path
from .views import *
from src.user.views import *

app_name = "access-portal-api"

urlpatterns = [
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("auth/signup/", CustomUserViewSet.as_view({"post": "create"}), name="signup"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="refresh"),
    path(
        "auth/user/activate/",
        CustomUserViewSet.as_view({"post": "activation"}),
        name="activate",
    ),
    path(
        "auth/user/resend_activation/",
        CustomUserViewSet.as_view({"post": "resend_activation"}),
        name="resend_activation",
    ),
    path(
        "auth/reset-password/",
        CustomUserViewSet.as_view({"post": "reset_password"}),
        name="reset_password",
    ),
    path(
        "auth/reset-password-confirm/",
        CustomUserViewSet.as_view({"post": "reset_password_confirm"}),
        name="reset_password_confirm",
    ),
    path("auth/users/me/", CustomUserViewSet.as_view({"get": "me"}), name="me"),
    path("access-key/", SchoolITPersonalAccessKeyView.as_view(), name="access-key"),
    path(
        "access-key/<str:keyTag>",
        SchoolITPersonalInactiveAccessKeyDeletionView.as_view(),
        name="access-key-deletion",
    ),
    path("admin/access-key/", AdminAccessKeyView.as_view(), name="admin-access-key"),
    path(
        "admin/school-active-key-lookup/<str:email>",
        SchoolActiveKeyLookup.as_view(),
        name="admin-school-access-info",
    ),
    path("admin/schools/", ListSchoolInfoView.as_view(), name="admin-list-school-info"),
]
