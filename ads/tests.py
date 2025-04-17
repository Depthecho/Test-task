from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Ad, ExchangeProposal
from .forms import AdForm


class AdsTestCase(TestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.user1 = User.objects.create_user(
            username='user1', password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='testpass123'
        )

        # Создаем тестовые объявления
        self.ad1 = Ad.objects.create(
            title='Ad 1',
            description='Description 1',
            category='books',
            condition='new',
            user=self.user1
        )
        self.ad2 = Ad.objects.create(
            title='Ad 2',
            description='Description 2',
            category='electronics',
            condition='used',
            user=self.user2
        )

        # Создаем тестовый клиент
        self.client = Client()

    def test_ad_create_authenticated(self):
        # Тест создания объявления аутентифицированным пользователем
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(reverse('ad_create'), {
            'title': 'New Ad',
            'description': 'New Description',
            'category': 'books',
            'condition': 'new'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ad.objects.count(), 3)

    def test_ad_edit_owner(self):
        # Тест редактирования объявления владельцем
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(reverse('ad_edit', args=[self.ad1.id]), {
            'title': 'Updated Ad 1',
            'description': 'Updated Description 1',
            'category': 'books',
            'condition': 'used'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Updated Ad 1')

    def test_ad_delete_owner(self):
        # Тест удаления объявления владельцем
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(reverse('ad_delete', args=[self.ad1.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ad.objects.count(), 1)

    def test_ad_delete_non_owner(self):
        # Тест, что нельзя удалить чужое объявление
        self.client.login(username='user2', password='testpass123')
        response = self.client.post(reverse('ad_delete', args=[self.ad1.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ad.objects.count(), 2)

    def test_ad_list_search(self):
        # Тест поиска объявлений
        response = self.client.get(reverse('ad_list'), {'search': 'Ad 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ad 1')
        self.assertNotContains(response, 'Ad 2')

    def test_ad_list_filter_category(self):
        # Тест фильтрации объявлений по категории
        response = self.client.get(reverse('ad_list'), {'category': 'books'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ad 1')
        self.assertNotContains(response, 'Ad 2')

    def test_ad_list_filter_condition(self):
        # Тест фильтрации объявлений по состоянию
        response = self.client.get(reverse('ad_list'), {'condition': 'used'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ad 2')
        self.assertNotContains(response, 'Ad 1')


class ExchangeProposalTestCase(TestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.user1 = User.objects.create_user(
            username='user1', password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='testpass123'
        )

        # Создаем тестовые объявления
        self.ad1 = Ad.objects.create(
            title='Ad 1',
            description='Description 1',
            category='books',
            condition='new',
            user=self.user1
        )
        self.ad2 = Ad.objects.create(
            title='Ad 2',
            description='Description 2',
            category='electronics',
            condition='used',
            user=self.user2
        )

        # Создаем тестовое предложение
        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Test comment'
        )

        # Создаем тестовый клиент
        self.client = Client()


class ServicesTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя и объявление
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.ad = Ad.objects.create(
            title='Test Ad',
            description='Test Description',
            category='books',
            condition='new',
            user=self.user
        )

    def test_create_ad(self):
        # Тест создания объявления через сервис
        from . import services
        form_data = {
            'title': 'New Ad',
            'description': 'New Description',
            'category': 'electronics',
            'condition': 'used'
        }
        form = AdForm(data=form_data)
        self.assertTrue(form.is_valid())
        ad = services.create_ad(form, self.user)
        self.assertEqual(ad.title, 'New Ad')
        self.assertEqual(ad.user, self.user)

    def test_get_user_ad_or_404(self):
        # Тест получения объявления пользователя
        from . import services
        ad = services.get_user_ad_or_404(self.ad.id, self.user)
        self.assertEqual(ad, self.ad)

    def test_delete_ad(self):
        # Тест удаления объявления
        from . import services
        services.delete_ad(self.ad)
        self.assertEqual(Ad.objects.count(), 0)

    def test_filter_ads(self):
        # Тест фильтрации объявлений
        from . import services
        from django.test import RequestFactory

        # Создаем тестовый запрос с параметрами поиска
        factory = RequestFactory()
        request = factory.get('/ads/', {'search': 'Test'})

        ads = services.filter_ads(request.GET)
        self.assertEqual(ads.count(), 1)
        self.assertEqual(ads[0].title, 'Test Ad')
