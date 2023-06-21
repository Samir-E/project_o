from django.db import models

# Create your models here.


class Positions(models.Model):
    """
    Товары из меню ресторана
    """
    position_name = models.CharField(
        'Название позиции',
        max_length=30,
    )
    position_price = models.DecimalField(
        'Цена позиции',
        default=0.00,
        max_digits=5,
        decimal_places=2,
    )
    image = models.ImageField(
        'Изображение позиции',
        upload_to='images_positions/',
        default='images_positions/default.jpg',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return self.position_name
