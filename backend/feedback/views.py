from rest_framework import viewsets
from rest_framework import permissions

from conf.permissions import IsStaffOrTargetUser
from feedback.models import BookFeedback
from feedback.serializers import BookFeedbackSerializer


# Create your views here.
class BookFeedbackViewSet(viewsets.ModelViewSet):
    queryset = BookFeedback.objects.all().order_by('-id')
    serializer_class = BookFeedbackSerializer

    def get_permissions(self):
        # разрешить пользователю, прошедшему проверку подлинности,
        # создавать с помощью POST
        return (permissions.IsAuthenticated()
                if self.request.method == 'POST' else IsStaffOrTargetUser()),
