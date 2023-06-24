from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema

from backend.utils.views import ActionSerializerMixin

from .models import OrderPosition, Orders
from .serializers import (
    OrderPositionSerializer,
    OrdersSerializer,
    UpdateOrderPositionSerializer,
    UpdateStatusOrderSerializer,
)


@extend_schema_view(
    retrieve=extend_schema(
        summary='Вернуть конкретный заказ по `id`',
    ),
    list=extend_schema(
        summary='Вернуть заказы.',
    ),
    create=extend_schema(
        summary='Создать заказ вместе с позициями.',
        description=(
            'Это API позволяет создать заказ вместе с позициями. Для этого в '
            '`positions` передаются объекты позиций. API возвращает 400 код, '
            'если в списке `positions` встречаются две или более одинаковых '
            'позиций.'
        )
    ),
    destroy=extend_schema(
        summary='Удалить заказ по `id`',
    ),
    change_order_status=extend_schema(
        summary='Изменить статус заказа.',
        description=(
            'Изменить статус конкретного заказа по `id`. API '
            'возвращает 400 код, если `completed`(завершенный) заказ был '
            'изменен.'
        ),
    ),
)
class OrdersViewSet(
    ActionSerializerMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для `Orders` модели.

    Это API доступно только для авторизованных пользователей.

    """
    queryset = Orders.objects.all().prefetch_related(
        'positions',
    )
    serializer_class = OrdersSerializer
    serializer_action_classes = {
        'change_order_status': UpdateStatusOrderSerializer,
    }

    @action(methods=['PATCH'], detail=True, url_path='update-status')
    def change_order_status(self, request, pk, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary='Вывести список всех позиций',
        description='Есть фильтрация по заказу. Смотреть параметры `Parameters`'
    ),
    retrieve=extend_schema(
        summary='Вернуть конкретную позицию по `id`',
    ),
    create=extend_schema(
        summary='Добавить позицию для конкретного заказа',
        description=(
            '`position` - id позиции\n'
            '`order` - id заказа\n'
            'Добавить позицию в заказ. При добавлении существующего заказа '
            'API возвращает 400 ошибку.'
        ),
    ),
    update=extend_schema(
        summary='Обновить количество заказанных позиций.',
    ),
    partial_update=extend_schema(
        summary='Обновить количество заказанных позиций.',
    ),
    delete=extend_schema(
        summary='Удалить позицию по `id`',
    ),
)
class OrderPositionActionsViewSet(
    ActionSerializerMixin,
    viewsets.ModelViewSet,
):
    """ViewSet для `OrderPosition` модели.

    Это API было доступно только для авторизованных пользователей.

    """
    queryset = OrderPosition.objects.all()
    serializer_class = OrderPositionSerializer
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    ordering = (
        '-id',
    )
    filterset_fields = (
        'order',
    )
    serializer_action_classes = {
        'update': UpdateOrderPositionSerializer,
    }
