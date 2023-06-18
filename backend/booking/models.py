from django.contrib.auth.models import User
from django.db import models

# Create your models here.
"""Бронирование столиков"""


class Booking(models.Model):
    """Модель заказа."""
    # ADOPTED = 'Принят'
    # CONFIRMED = 'Подтвержден'
    # CANCELLED = 'Отменен'
    # COMPLITED = 'Выполнен'

    # BOOKING_STATUS_CHOISE = [
    #     (ADOPTED, 'Принят'),
    #     (CONFIRMED, 'Подтвержден'),
    #     (CANCELLED, 'Отменен'),
    #     (COMPLITED, 'Выполнен'),
    # ]

    fio = models.CharField(
        verbose_name='ФИО',
        max_length=40,
    )
    mobile_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=12,
        help_text='+7**********',
    )
    # booking_status = models.CharField('Статус брони', max_length=11,
    #                                   choices=BOOKING_STATUS_CHOISE,
    #                                   default=ADOPTED)
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
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
