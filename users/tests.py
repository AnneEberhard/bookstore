from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser


class AuthTokenTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def test_token_obtain_pair(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']

        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_blacklist(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']

        # Blacklist the token
        url = reverse('token_blacklist')
        response = self.client.post(url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to refresh the blacklisted token
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterTests(APITestCase):

    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'first_name': 'First',
            'last_name': 'Last',
            'author_pseudonym': 'Pseudonym'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(response.data['message'], 'User registered successfully.')
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())
