import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal

from .models import Positions


class PositionsFactory(DjangoModelFactory):
    position_name = factory.Faker('word')
    position_price = FuzzyDecimal(low=0.0, high=1000.0)

    class Meta:
        model = Positions
