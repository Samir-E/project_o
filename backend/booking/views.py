from rest_framework import viewsets, permissions


from conf.permissions import IsStaffOrTargetUser
from booking.serializers import BookingSerializer
from booking.models import Booking


# Create your views here.


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-id')
    serializer_class = BookingSerializer

    def get_permissions(self):
        # разрешить пользователю, прошедшему проверку подлинности,
        # создавать с помощью POST
        return (permissions.IsAuthenticated()
                if self.request.method == 'POST' else IsStaffOrTargetUser()),




