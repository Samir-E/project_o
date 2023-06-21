import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from backend.menu.factories import PositionsFactory
from backend.utils.url import reverse_lazy

from ...factories import OrderFactory, OrderPositionFactory
from ...models import OrderPosition, Orders


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_retrieve_order(api_client: APIClient, order: Orders):
    response: Response = api_client.get(
        path=reverse_lazy('api:cart-detail', kwargs={'pk': order.pk}),
    )
    data = response.data

    assert response.status_code == status.HTTP_200_OK
    assert len(data['positions']) == 3
    assert data['total_price'] == order.total_price
    assert data['status'] == order.status


@pytest.mark.django_db
def test_retrieve_order_wo_permissions(api_client: APIClient, order: Orders):
    response: Response = api_client.get(
        path=reverse_lazy('api:cart-detail', kwargs={'pk': order.pk}),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_create_new_order(api_client: APIClient):
    position_1, position_2 = PositionsFactory.create_batch(size=2)

    response: Response = api_client.post(
        path=reverse_lazy('api:cart-list'),
        data={
            'positions': [
                {
                    'position': position_1.id,
                    'servings': 10,
                },
                {
                    'position': position_2.id,
                    'servings': 10,
                },
            ],
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    expected_order = Orders.objects.get(id=data['id'])

    assert len(data['positions']) == 2
    assert float(data['total_price']) == expected_order.total_price
    assert data['status'] == expected_order.status

    position_data = data['positions'][0]
    expected_position = OrderPosition.objects.get(id=position_data['id'])
    assert position_data['cost'] == expected_position.cost
    assert position_data['servings'] == expected_position.servings


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_create_new_order_duplicate_position(api_client: APIClient):
    position = PositionsFactory()

    response: Response = api_client.post(
        path=reverse_lazy('api:cart-list'),
        data={
            'positions': [
                {
                    'position': position.id,
                    'servings': 10,
                },
                {
                    'position': position.id,
                    'servings': 10,
                },
            ],
        },
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_create_new_order_wo_position(api_client: APIClient):
    response: Response = api_client.post(
        path=reverse_lazy('api:cart-list'),
        data={
            'positions': None,
        },
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_list_order_positions(api_client: APIClient, order: Orders):
    response: Response = api_client.get(
        path=reverse_lazy(
            'api:orderposition-list',
            query={'order': order.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.data

    expected_order_positions = OrderPosition.objects.filter(order_id=order.id)
    expected_ids = set([item.id for item in expected_order_positions])
    assert set([item['id'] for item in data]) == expected_ids


@pytest.mark.django_db
def test_list_order_positions_wo_permissions(api_client: APIClient):
    response: Response = api_client.get(reverse_lazy('api:orderposition-list'))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_create_order_positions(api_client: APIClient):
    order = OrderFactory()
    position = PositionsFactory()

    response: Response = api_client.post(
        path=reverse_lazy('api:orderposition-list'),
        data={
            'order': order.id,
            'position': position.id,
            'servings': 10,
        },
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_create_order_positions_duplicate(api_client: APIClient):
    order_positions = OrderPositionFactory()

    response: Response = api_client.post(
        path=reverse_lazy('api:orderposition-list'),
        data={
            'order': order_positions.order.id,
            'position': order_positions.position.id,
            'servings': 10,
        },
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_update_order_positions(api_client: APIClient):
    order_positions = OrderPositionFactory()
    new_servings_value = order_positions.servings + 1

    response: Response = api_client.put(
        path=reverse_lazy(
            'api:orderposition-detail',
            kwargs={'pk': order_positions.id},
        ),
        data={'servings': new_servings_value},
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['servings'] == new_servings_value


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_delete_order_positions(api_client: APIClient):
    order_positions = OrderPositionFactory()

    response: Response = api_client.delete(
        path=reverse_lazy(
            'api:orderposition-detail',
            kwargs={'pk': order_positions.id},
        ),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_update_completed_order(api_client: APIClient, order: Orders):
    order.status = Orders.COMPLETED
    order.save()

    response: Response = api_client.patch(
        path=reverse_lazy(
            'api:cart-change-order-status',
            kwargs={'pk': order.id},
        ),
        data={'status': order.CONFIRMED},
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.usefixtures('user_authenticated')
def test_update_order_status(api_client: APIClient, order: Orders):
    response: Response = api_client.patch(
        path=reverse_lazy(
            'api:cart-change-order-status',
            kwargs={'pk': order.id},
        ),
        data={'status': order.COMPLETED},
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
