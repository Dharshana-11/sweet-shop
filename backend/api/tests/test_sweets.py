from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

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