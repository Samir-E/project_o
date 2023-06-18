from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r'', views.OrderViewSet,)
router.register(r'', views.OrderPositionViewSet,)

urlpatterns = [
    path(r'', include(router.urls))
    # path(r'add/', AddItemToCartView.as_view(), name='add_cart_item'),
    # path(r'delete/', RemoteItemFromCartView.as_view(), name='remove_cart_item'),
    # path(r'total/', CartTotalPriceView.as_view(), name='total_cart_price')
]


