from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'', views.PositionViewSet,)

urlpatterns = [
    path('', include(router.urls)),
]


