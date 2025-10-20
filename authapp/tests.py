from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile

class AuthAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'  # Update this if your URL is different
        self.login_url = '/api/login/'
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration_creates_profile(self):
        """Ensure registering a user also creates a UserProfile."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='testuser')
        profile_exists = UserProfile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists, "UserProfile should be created automatically")

    def test_user_login_successful(self):
        """Ensure user can log in after registration."""
        User.objects.create_user(username='loginuser', email='login@example.com', password='login123')
        response = self.client.post(self.login_url, {'username': 'loginuser', 'password': 'login123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data, "Login response should contain an authentication token")

    def test_user_login_invalid_credentials(self):
        """Ensure invalid login credentials are rejected."""
        response = self.client.post(self.login_url, {'username': 'wrong', 'password': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
