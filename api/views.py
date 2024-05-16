from django.contrib.auth import get_user_model
from src.key.models import AccessKey
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .utils import generateAccessKey, sendEmail
from datetime import datetime, timedelta
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .paginator import QueryResultPagination

User = get_user_model()


# School's IP personne; API Views
class SchoolITPersonalAccessKeyView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pagination_class = QueryResultPagination

    @extend_schema(
        methods=["GET"],
        summary="Get access key(s)",
        description="Get access key(s). Optionally: Filter by 'key-tag' or 'status' of a key",
        tags=["SCH IT Personnel"],
        responses={200: AccessKeySerializerDocsView(many=True), 404: None},
        parameters=[
            OpenApiParameter(
                "key-tag",
                location=OpenApiParameter.QUERY,
                description="Filter by key-tag",
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                "status",
                location=OpenApiParameter.QUERY,
                description="Filter by status",
                type=OpenApiTypes.STR,
            ),
        ],
    )
    @method_decorator(cache_page(5))  # 5 seconds
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        user = request.user
        key_tag = request.query_params.get("key-tag", None)
        keyStatus = request.query_params.get("status", None)

        keys = AccessKey.objects.filter(owner=user)

        if key_tag:
            try:
                key = AccessKey.objects.get(owner=user, key_tag=key_tag)
            except AccessKey.DoesNotExist:
                return Response(
                    {"error": f"Key ({key_tag}) not found!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = AccessKeySerializer(key)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if keyStatus:
            keys = keys.filter(status=keyStatus)
            if keys.count() == 0:
                return Response(
                    {"error": f"No {keyStatus} keys found!"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # paginating results if more than 10
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(keys, request)

        serializer = AccessKeySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        methods=["POST"],
        summary="Create an access key",
        description="Create an access key. Note: You must not an 'active' access key!",
        tags=["SCH IT Personnel"],
        responses={204: AccessKeySerializerDocsView(), 400: None},
        request=AccessKeySerializerDocsPOST,
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        key_tag = request.data.get("key_tag", None)
        validity_duration_days = request.data.get("validity_duration_days", None)
        validity_duration_months = request.data.get("validity_duration_months", None)

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

        if AccessKey.objects.filter(key_tag=key_tag).exists():
            return Response(
                {"error": "Key-tag already taken!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if validity_duration_days and validity_duration_months:
            return Response(
                {
                    "error": "Duration can be 'validity-duration-days' or 'validity-duration-months'"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if validity_duration_days:
            calculated_validity_duration_days = int(validity_duration_days)
            if not 0 < calculated_validity_duration_days <= 365:
                return Response(
                    {
                        "error": "Validity duration must be between 1 and 365 days inclusive"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif validity_duration_months:
            calculated_validity_duration_days = int(validity_duration_months) * 30
            if not 0 < calculated_validity_duration_days <= 365:
                return Response(
                    {
                        "error": "Validity duration must be between 1 and 12 months inclusive"
                    },
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


class SchoolITPersonalInactiveAccessKeyDeletionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        methods=["DELETE"],
        summary="Delete an inactive access key",
        description=" Delete an 'inactive' access key. The status of the key must be 'inactive' to use this endpoint",
        tags=["SCH IT Personnel"],
        responses={204: None, 400: None, 404: None},
    )
    def delete(self, request, keyTag=None, *args, **kwargs):
        user = request.user
        key_tag = keyTag
        if key_tag is None:
            return Response(
                {"error": "Key-tag is required in path!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            key = AccessKey.objects.get(owner=user, key_tag=key_tag)
        except AccessKey.DoesNotExist:
            return Response(
                {"error": f"Key ({key_tag}) not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if key.status == "revoked":
            return Response(
                {
                    "error": f"Access key '{key_tag}' has been revoked! Note: You can only delete inactive keys"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if key.status == "expired":
            return Response(
                {
                    "error": f"Access key ({key_tag}) has expired! Note: You can only delete inactive keys"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if key.status in ["active", "revoked", "expired"]:
            return Response(
                {"error": f"Status of '{key_tag}' must be inactive!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        key.delete()
        return Response(
            {"message": f"Inactive key deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


# Admin API Vie
class AdminAccessKeyView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pagination_class = QueryResultPagination

    @extend_schema(
        methods=["GET"],
        summary="List access keys of School IT personnel(s)",
        description="List all access keys of all School IT personnels or a particular IT personnel. Optionally: Filter by 'status', 'owner', or 'key-tag' of an access key",
        tags=["Admin"],
        responses={200: AdminAccessKeySerializer(many=True), 400: None},
        parameters=[
            OpenApiParameter(
                "status",
                description="Filter by 'status' of access keys",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                "owner",
                description="Filter by 'owner' of access keys",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                "key-tag",
                description="Filter by 'key-tag' of access keys",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    @method_decorator(cache_page(5))  # 5 seconds
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        keyStatus = request.query_params.get("status", None)
        owner = request.query_params.get("owner", None)
        key_tag = request.query_params.get("key-tag", None)

        keys = AccessKey.objects.all()

        if keyStatus:
            keys = keys.filter(status=keyStatus)
        if owner:
            try:
                user = User.objects.get(email=owner)
            except User.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            keys = keys.filter(owner=user)
        if key_tag:
            keys = keys.filter(key_tag=key_tag)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(keys, request)

        serializer = AdminAccessKeySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        methods=["POST"],
        summary="Activate an access key",
        description="Activate an access key to allow usage by a School IT personnel",
        tags=["Admin"],
        responses={204: None, 400: None},
        request=AdminAccessKeySerializerDocsActionView,
    )
    def post(self, request):
        userEmail = request.data.get("email", None)
        keyTag = request.data.get("key_tag", None)

        if not keyTag and not userEmail:
            return Response(
                {"error": "Email and key-tag are required to activate a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not userEmail:
            return Response(
                {"error": "Email is required to activate a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not keyTag:
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
            key = AccessKey.objects.get(owner=user, status="inactive", key_tag=keyTag)
        except AccessKey.DoesNotExist:
            return Response(
                {"error": f"Status of '{keyTag}' should be inactive to activate it!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        key.status = "active"

        activation_date = timezone.now()
        expiry_date = activation_date + timedelta(days=key.validity_duration_days)

        key.procurement_date = activation_date
        key.expiry_date = expiry_date
        key.save()

        expiry_date_formatted = expiry_date.strftime("%d %B, %Y %H:%M %p")
        data = {
            "key": key.key,
            "key_tag": keyTag,
            "expiry_date": expiry_date_formatted,
            "owner": user.full_name,
            "validity_days": key.validity_duration_days,
        }
        sendEmail(accessGranted=True, recipient=user.email, keyData=data)
        return Response(
            {"message": "Key activated successfully"},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        methods=["PUT"],
        summary="Revoke an access key",
        description="Revoke an active access key to deny usage by a School IT personnel",
        tags=["Admin"],
        responses={200: None, 400: None},
        request=AdminAccessKeySerializerDocsActionView,
    )
    def put(self, request):
        userEmail = request.data.get("email", None)
        keyTag = request.data.get("key_tag", None)

        if not keyTag and not userEmail:
            return Response(
                {"error": "Email and key-tag are required to revoke a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not userEmail:
            return Response(
                {"error": "Email is required to revoke a key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not keyTag:
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
            key = AccessKey.objects.get(owner=user, status="active", key_tag=keyTag)
        except AccessKey.DoesNotExist:
            return Response(
                {"error": f"Status of '{keyTag}' should be active to revoke it!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        key.status = "revoked"
        key.save()

        data = {
            "owner": user.full_name,
            "key_tag": keyTag,
        }
        sendEmail(KeyRevoked=True, recipient=user.email, keyData=data)
        return Response(
            {"message": "Key revoked successfully"},
            status=status.HTTP_200_OK,
        )


class SchoolActiveKeyLookup(APIView):
    permission_classes = [IsAdminUser]

    schooEmail = OpenApiParameter(
        "schooleEmail",
        location=OpenApiParameter.QUERY,
        description="School email",
        type=OpenApiTypes.STR,
    )

    @extend_schema(
        methods=["GET"],
        summary="Lookup school's active key info",
        description="Get school access key info by providing the school's email",
        tags=["Admin"],
        responses={200: AdminSchoolActiveKeyLookUpSerializer(), 400: None, 404: None},
        parameters=[schooEmail],
    )
    def get(self, request, email=None, *args, **kwargs):
        if not email:
            return Response(
                {"error": "School email is required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            active_key = AccessKey.objects.get(owner=user, status="active")
            serializer = AdminSchoolActiveKeyLookUpSerializer(active_key)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessKey.DoesNotExist:
            return Response(
                {"error": "No active key found for this user"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ListSchoolInfoView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pagination_class = QueryResultPagination

    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_active=True)

    @extend_schema(
        responses=AdminUserViewSerializer(many=True),
        tags=["Admin"],
        summary="List all school users",
        description="This endpoint lists all school IT personnels",
    )
    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        # paginating results if more than 10
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(users, request)

        serializer = AdminUserViewSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
