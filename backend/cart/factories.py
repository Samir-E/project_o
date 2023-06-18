import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from backend.menu.factories import PositionsFactory

from ..factories import UserFactory
from .models import OrderPosition, Orders


class OrderFactory(DjangoModelFactory):
    """Factory for `Orders` model."""
    create_order = factory.Faker(
        'date_time',
        tzinfo=timezone.get_current_timezone(),
    )
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Orders


class OrderPositionFactory(DjangoModelFactory):
    """Factory for `OrderPosition` model."""
    order = factory.SubFactory(OrderFactory)
    position = factory.SubFactory(PositionsFactory)
    servings = FuzzyInteger(low=0, high=10)

    class Meta:
        model = OrderPosition
