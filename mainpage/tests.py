from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AuthServiceIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

    def test_register_user_success(self):
        response = self.client.post(reverse('register'), self.register_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

    def test_login_user_success(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(reverse('login'), self.login_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_user(self):
        User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)