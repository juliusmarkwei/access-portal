from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse
from src.key.models import AccessKey

User = get_user_model()


class SchoolITPersonalAccessKeyViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            password="test_password",
            phone="1234567890",
            email="1234567890",
            full_name="test_user",
        )
        self.user.is_active = True  # Activate the user
        self.user.save()

        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="admin_password",
            phone="1234567890",
            full_name="admin",
        )
        self.admin_user.is_active = True  # Activate the admin user
        self.admin_user.save()

        self.token = self.get_access_token(self.user)
        self.admin_token = self.get_access_token(self.admin_user)

    def get_access_token(self, user):
        return str(AccessToken.for_user(user))

    def test_get_access_key(self):
        url = reverse(
            "access-portal-api:access-key"
        )  # Replace with your actual endpoint
        response = self.client.get(url, HTTP_AUTHORIZATION=f"JWT {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_access_key(self):
        url = reverse("access-portal-api:access-key")
        data = {"key_tag": "test_key", "validity_duration_days": 30}
        response = self.client.post(
            url, data, format="json", HTTP_AUTHORIZATION=f"JWT {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test if trying to create another key returns an error
        response = self.client.post(
            url, data, format="json", HTTP_AUTHORIZATION=f"JWT {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SchoolITPersonalInactiveAccessKeyDeletionViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            password="test_password",
            email="test@example.com",
            full_name="test_user",
            phone="1234567890",
        )
        self.user.is_active = True  # Activate the user
        self.user.save()
        self.token = self.get_access_token(self.user)

    def get_access_token(self, user):
        return str(AccessToken.for_user(user))

    def create_inactive_access_key(self):
        # Create an inactive access key for the user
        return AccessKey.objects.create(
            owner=self.user, key_tag="test_key", status="inactive"
        )

    def test_delete_inactive_access_key(self):
        # Create an inactive access key
        access_key = self.create_inactive_access_key()
        url = reverse(
            "access-portal-api:access-key-deletion",
            kwargs={"keyTag": access_key.key_tag},
        )

        response = self.client.delete(url, HTTP_AUTHORIZATION=f"JWT {self.token}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_inactive_access_key_not_found(self):
        # Try to delete an inactive access key that doesn't exist
        url = reverse(
            "access-portal-api:access-key-deletion",
            kwargs={"keyTag": "non_existent_key_tag"},
        )

        response = self.client.delete(url, HTTP_AUTHORIZATION=f"JWT {self.token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_active_access_key(self):
        # Create an active access key
        access_key = AccessKey.objects.create(
            owner=self.user, key_tag="active_key", status="active"
        )
        url = reverse(
            "access-portal-api:access-key-deletion",
            kwargs={"keyTag": access_key.key_tag},
        )

        response = self.client.delete(url, HTTP_AUTHORIZATION=f"JWT {self.token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Status of 'active_key' must be inactive!"
        )
