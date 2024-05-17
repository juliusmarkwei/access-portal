from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from src.key.models import AccessKey

User = get_user_model()


class AdminAccessKeyViewTests(APITestCase):
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

    def test_list_access_keys(self):
        url = reverse("access-portal-api:admin-access-key")

        response = self.client.get(url, HTTP_AUTHORIZATION=f"JWT {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_access_key(self):
        url = reverse("access-portal-api:admin-access-key")

        # Create a user and an inactive access key
        user = User.objects.create_user(
            email="test@example.com",
            password="test_password",
            full_name="Test User",
            phone="1234567890",
            is_active=True,
        )
        access_key = AccessKey.objects.create(
            owner=user, key_tag="test_key", status="inactive"
        )

        data = {"email": user.email, "key_tag": access_key.key_tag}
        response = self.client.post(
            url, data, format="json", HTTP_AUTHORIZATION=f"JWT {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_revoke_access_key(self):
        url = reverse("access-portal-api:admin-access-key")

        # Create a user and an active access key
        user = User.objects.create_user(
            email="test@example.com",
            password="test_password",
            full_name="Test User",
            phone="1234567890",
            is_active=True,
        )
        access_key = AccessKey.objects.create(
            owner=user, key_tag="test_key", status="active"
        )

        data = {"email": user.email, "key_tag": access_key.key_tag}
        response = self.client.put(
            url, data, format="json", HTTP_AUTHORIZATION=f"JWT {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
