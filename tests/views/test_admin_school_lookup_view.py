from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from src.key.models import AccessKey

User = get_user_model()


class SchoolActiveKeyLookupTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="admin_password",
            phone="1234567890",
            full_name="Admin User",
        )
        self.admin_user.is_active = True
        self.admin_user.save()
        self.token = self.get_access_token(self.admin_user)

    def get_access_token(self, user):
        return str(AccessToken.for_user(user))

    def test_lookup_school_active_key_info(self):
        # Create a user and an active access key
        user = User.objects.create_user(
            email="school@example.com",
            password="school_password",
            full_name="School User",
            phone="1234567890",
            is_active=True,
        )
        access_key = AccessKey.objects.create(
            owner=user, key_tag="test_key", status="active"
        )

        url = reverse(
            "access-portal-api:admin-school-access-info", kwargs={"email": user.email}
        )
        response = self.client.get(url, HTTP_AUTHORIZATION=f"JWT {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lookup_school_active_key_info_invalid_email(self):
        # Provide an invalid email as query parameter
        url = reverse(
            "access-portal-api:admin-school-access-info",
            kwargs={"email": "invalid@example.com"},
        )
        response = self.client.get(url, HTTP_AUTHORIZATION=f"JWT {self.token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
