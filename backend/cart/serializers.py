from typing import Mapping

from django.db.utils import IntegrityError
from rest_framework import serializers

from .models import OrderPosition, Orders


class OrderPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPosition
        fields = (
            'id',
            'position',
            'order',
            'servings',
            'cost',
        )
        read_only_fields = (
            'cost',
        )


class NestedOrderPositionSerializer(OrderPositionSerializer):
    class Meta(OrderPositionSerializer.Meta):
        read_only_fields = (
            'order',
            'cost',
        )


class UpdateOrderPositionSerializer(OrderPositionSerializer):
    class Meta(OrderPositionSerializer.Meta):
        read_only_fields = (
            'position',
            'order',
            'cost',
        )


class OrdersSerializer(serializers.ModelSerializer):
    """Serializer for `Order` model."""
    positions = NestedOrderPositionSerializer(
        many=True,
        allow_null=True,
        required=False,
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Orders
        fields = (
            'id',
            'positions',
            'total_price',
            'create_order',
            'status',
            'user',
        )
        read_only_fields = (
            'user',
            'total_price',
        )

    def create(self, validated_data):
        """Override create method to provide creation of linked objects.

        Create `OrderPosition` instances for an `Order` instance.

        """
        positions = validated_data.pop('positions', None) or []
        instance = super().create(validated_data)

        try:
            OrderPosition.objects.bulk_create([
                OrderPosition(
                    order=instance,
                    **position,
                )
                for position in positions
            ])
        except IntegrityError as error:
            raise serializers.ValidationError(
                {'positions': error},
                code='unique_positions_violated',
            )

        return instance


class UpdateStatusOrderSerializer(OrdersSerializer):
    def __init__(self, *args, **kwargs):
        """Override init method to make `positions` read-only."""
        self.fields['positions'].read_only = True
        super().__init__(*args, **kwargs)

    class Meta(OrdersSerializer.Meta):
        read_only_fields = (
            'id',
            'positions',
            'total_price',
            'create_order',
            'user',
        )

    def validate(self, attrs: Mapping[str, str]) -> Mapping[str, str]:
        validated_data = super().validate(attrs)
        status = validated_data['status']
        self.instance.status = status
        self.instance.full_clean()
        return validated_data
