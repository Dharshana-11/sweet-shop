from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class RegisterTestUser(APITestCase):
    def test_user_registration(self):
        # Get URL for the registe endpoint
        url = reverse('register')

        # Mock data for test user
        data = {
            "username" : "testuser",
            "password" : "test@123"
        }

        # POST request sent along with JSON data
        response = self.client.post(url, data, format="json")

        # Checks whether server responded with 201, if yes it passes silently; if no then will raise an error
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)