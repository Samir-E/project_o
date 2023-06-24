from rest_framework import permissions, viewsets

from backend.booking.models import Booking
from backend.booking.serializers import BookingSerializer
from backend.conf.permissions import IsStaffOrTargetUser

# Create your views here.


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-id')
    serializer_class = BookingSerializer

    def get_permissions(self):
        # разрешить любому пользователю, создавать с помощью POST
        return (permissions.AllowAny()
                if self.request.method == 'POST' else IsStaffOrTargetUser()),
