from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class SweetsAuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "sweetuser",
            password = "sweet@123"
        )

        self.url = reverse("sweets-list")
    
    def test_sweets_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class CreateSweetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "sweetuser",
            password = "sweet@123"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION = f"Bearer {str(refresh.access_token)}"
        )

        self.url = reverse("sweets-list")
    
    def test_create_sweet(self):
        data = {
            "name": "Ladoo",
            "category": "Indian",
            "price": 10.0,
            "quantity": 100
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)