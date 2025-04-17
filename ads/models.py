from django.db import models
from django.contrib.auth.models import User

# Модель объявления
class Ad(models.Model):
    CONDITION_CHOICES = [
        ('new', 'новый'),
        ('used', 'б/у'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')  # Владелец объявления
    title = models.CharField(max_length=255)  # Заголовок
    description = models.TextField()  # Описание
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)  # Фото (необязательное)
    category = models.CharField(max_length=100)  # Категория
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)  # Состояние вещи
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f'{self.title} ({self.user.username})'  # Для отображения в админке и отладке

# Модель предложения обмена
class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')  # Кто предлагает
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')  # Кому предлагает
    comment = models.TextField()  # Сообщение к предложению
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Статус
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f'{self.ad_sender} → {self.ad_receiver} [{self.status}]'

    def is_accepted(self):
        return self.status == 'accepted'

    def is_rejected(self):
        return self.status == 'rejected'
