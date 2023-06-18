from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(
    r'orders',
    viewset=views.OrdersViewSet,
    basename='cart',
)
router.register(
    r'orders-positions',
    viewset=views.OrderPositionActionsViewSet,
)


urlpatterns = [
    path(r'', include(router.urls)),
]
