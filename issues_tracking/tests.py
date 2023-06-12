from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class SignupTest(APITestCase):
    def setUp(self):
        self.url = reverse('signup-list')
        self.valid_payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        self.invalid_payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
        }

    def test_create_account_with_valid_payload(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.valid_payload["email"]).exists())

    def test_create_account_with_invalid_payload(self):
        response = self.client.post(self.url, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_with_duplicate_email(self):
        self.client.post(self.url, self.valid_payload)
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
