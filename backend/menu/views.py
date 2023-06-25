from rest_framework import viewsets

from ..conf.permissions import IsAdminUserOrReadOnly
from .models import Positions
from .serializers import PositionSerializer

# Create your views here.


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Positions.objects.all().order_by('id')
    serializer_class = PositionSerializer
    permission_classes = [IsAdminUserOrReadOnly]
