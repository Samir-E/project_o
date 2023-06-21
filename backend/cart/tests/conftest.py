import pytest

from ..factories import OrderFactory, OrderPositionFactory
from ..models import Orders


@pytest.fixture(scope='function')
def order() -> Orders:
    """Create an order with 3 positions."""
    order = OrderFactory()
    OrderPositionFactory.create_batch(size=3, order=order)
    return order
