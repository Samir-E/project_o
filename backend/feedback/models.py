from django.contrib.auth.models import User
from django.db import models

# Create your models here.
"""
Книга отзывов
"""


class BookFeedback(models.Model):
    fio = models.CharField('ФИО', max_length=40)
    email = models.EmailField('Электронная почта', max_length=30)
    feedback_comment = models.TextField('Комментарий', max_length=255)
    date_record = models.DateTimeField('Дата и время отзыва',
                                       auto_now_add=True)
    autor = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
