from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AuthViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')

        self.user_credentials = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        }

    def test_register_user_success(self):
        # Успешная регистрация
        response = self.client.post(self.register_url, data=self.user_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_password_mismatch(self):
        # Регистрация с разными паролями
        data = self.user_credentials.copy()
        data['confirm_password'] = 'wrongpassword'
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_login_user_success(self):
        # Успешный вход
        User.objects.create_user(username='testuser', password='securepassword123')
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'securepassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_user_invalid_credentials(self):
        # Вход с неверными данными
        response = self.client.post(self.login_url, {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_user(self):
        # Выход пользователя
        user = User.objects.create_user(username='testuser', password='securepassword123')
        self.client.login(username='testuser', password='securepassword123')
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_home_page_accessible(self):
        # Проверка доступности главной страницы
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainpage/home_page.html')
