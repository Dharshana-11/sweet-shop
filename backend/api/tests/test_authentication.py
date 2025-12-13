from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
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

class LoginTestUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "testuser",
            password = "test@123"
        )

        self.url = reverse("login")
    
    def test_login_success(self):
        data = {
            "username" : "testuser",
            "password" : "test@123" 
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self):
        data = {
            "username" : "testuser",
            "password" : "wrong@password"
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
