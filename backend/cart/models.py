from dirtyfields import DirtyFieldsMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Orders(DirtyFieldsMixin, models.Model):
    """История заказов"""
    NOT_CONFIRMED = 'not_confirmed'
    CONFIRMED = 'confirmed'
    IN_PROGRESS = 'in progress'
    COMPLETED = 'completed'

    STATUS_CHOICES = (
        (NOT_CONFIRMED, _('Not confirmed')),
        (CONFIRMED, _('Confirmed')),
        (IN_PROGRESS, _('An order is in progress')),
        (COMPLETED, _('An order is completed')),
    )

    create_order = models.DateTimeField(
        verbose_name='Дата и время заказа',
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name=_('Order status'),
        default=NOT_CONFIRMED,
    )
    user = models.ForeignKey(
        to=User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = verbose_name

    @property
    def total_price(self) -> float:
        positions = self.positions.all()
        return sum([position.cost for position in positions])

    def clean(self) -> None:
        """Prohibit to change `completed` orders.

        Raises:
            ValidationError if an instance is changed when it has `completed`
                status

        """
        dirty_fields = self.get_dirty_fields(check_relationship=True)
        is_completed = (
            dirty_fields.get('status', None) == self.COMPLETED
        )
        if is_completed and dirty_fields:
            raise ValidationError({
                'status': _(
                    f'An order (id = {self.id}) with `completed` '
                    'status is unchangeable'
                ),
            })

        super().clean()


class OrderPosition(models.Model):
    """Информация заказа"""
    position = models.ForeignKey(
        to='menu.Positions',
        related_name='order_positions',
        on_delete=models.PROTECT,
    )
    order = models.ForeignKey(
        to='cart.Orders',
        related_name='positions',
        on_delete=models.DO_NOTHING,
        verbose_name=_('Orders'),
        null=True,
    )
    servings = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
    )

    class Meta:
        verbose_name = 'Информация о заказе'
        verbose_name_plural = verbose_name
        unique_together = (('position', 'order'), )

    @property
    def cost(self) -> float:
        """Property to get total cost by position."""
        return float(self.position.position_price) * self.servings
