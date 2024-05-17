from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.serializers import AdminUserViewSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone

User = get_user_model()


class ListSchoolInfoViewTests(APITestCase):
    def setUp(self):
        # Create an admin user
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

    def test_list_school_users(self):
        # Create two school users
        school_user1 = User.objects.create_user(
            email="user1@example.com",
            password="user1_password",
            full_name="School User 1",
            phone="1234567890",
            is_admin=False,
            is_active=True,
        )
        school_user2 = User.objects.create_user(
            email="user2@example.com",
            password="user2_password",
            full_name="School User 2",
            phone="1234567890",
            is_admin=False,
            is_active=True,
        )

        # URL for the API endpoint
        url = reverse("access-portal-api:admin-list-school-info")

        # Authenticate the request with the admin user's token
        response = self.client.get(url, HTTP_AUTHORIZATION=f"JWT {self.token}")

        # Check if the response status code is 200 OK

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the expected number of users
        self.assertEqual(len(response.data["results"]), 2)

        # Get the serialized data from the response
        serialized_data = response.data["results"]

        # Check if each user's email and full name is in the serialized data
        user_data_list = [
            {
                "email": school_user1.email,
                "full_name": school_user1.full_name,
                "phone": school_user1.phone,
                "is_active": school_user1.is_active,
                "created_at": school_user1.created_at.strftime("%d %b, %Y %I:%M %p"),
            },
            {
                "email": school_user2.email,
                "full_name": school_user2.full_name,
                "phone": school_user2.phone,
                "is_active": school_user2.is_active,
                "created_at": school_user2.created_at.strftime("%d %b, %Y %I:%M %p"),
            },
        ]
        for user_data in user_data_list:
            self.assertIn(user_data, serialized_data)
