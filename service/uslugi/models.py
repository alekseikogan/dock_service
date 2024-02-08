from django.db import models
from django.core.validators import MaxValueValidator

from clients.models import Client

class Service(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Стоимость')

    class Meta:
        db_table = 'services'
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'
    
    def __str__(self):
        return self.name


class Plan(models.Model):
    PlAN_TYPES = (
        ('full', 'Полная'),
        ('student', 'Студенческая'),
        ('discount', 'Скидочная'),
    )

    plan_type = models.CharField(
        max_length=20,
        choices=PlAN_TYPES,
        verbose_name='Тип подписки',)
    discount_percent = models.PositiveIntegerField(
        verbose_name='Процент скидки',
        default=0,
        validators=[MaxValueValidator(100)])

    class Meta:
        db_table = 'plans'
        verbose_name = 'План'
        verbose_name_plural = 'Планы'
    
    def __str__(self):
        return f'{self.plan_type} - {self.discount_percent}%'


class Subscription(models.Model):
    client = models.ForeignKey(
        Client,
        related_name='subscriptions',
        on_delete=models.PROTECT,
        verbose_name='Клиент')

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name='Сервис')
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name='План')

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
    
    def __str__(self):
        return f'{self.client} - {self.service} - {self.plan}'