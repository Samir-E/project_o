from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Booking(models.Model):
    """Бронирование столиков"""

    fio = models.CharField(
        verbose_name='ФИО',
        max_length=40,
    )
    mobile_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=12,
        help_text='+7**********',
    )
    booking_comment = models.TextField(
        verbose_name='Комментарий',
        max_length=255,
        help_text='Столик: *, Количество гостей: *',
    )
    date_booking = models.DateTimeField(
        verbose_name='Дата и время брони',
    )
    date_reg = models.DateTimeField(
        verbose_name='Дата и время регистрации брони',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
