from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from src.user.models import User as CustomUser
from uuid import uuid4
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import AccessToken


class AuthEndpointsTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "test_password",
            "full_name": "Test User",
            "phone": "1234567890",
            "is_active": True,
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.token = self.get_access_token(self.user)

    def get_access_token(self, user):
        return str(AccessToken.for_user(user))

    def test_login(self):
        url = reverse("access-portal-api:login")
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        url = reverse("access-portal-api:refresh")
        data = {"refresh": str(refresh)}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)

    def test_signup(self):
        url = reverse("access-portal-api:signup")
        new_user_data = {
            "email": "new_user@example.com",
            "password": "new_password",
            "re_password": "new_password",  # Added to match the serializer's "re_password" field
            "full_name": "New User",
            "phone": "1234567890",
        }
        response = self.client.post(url, new_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_me(self):
        self.client.force_login(self.user)
        url = reverse("access-portal-api:me")
        response = self.client.get(url, HTTP_AUTHORIZATION=f"JWT {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
