from rest_framework import permissions, viewsets

from backend.conf.permissions import IsStaffOrTargetUser
from backend.feedback.models import BookFeedback
from backend.feedback.serializers import BookFeedbackSerializer


# Create your views here.
class BookFeedbackViewSet(viewsets.ModelViewSet):
    queryset = BookFeedback.objects.all().order_by('-id')
    serializer_class = BookFeedbackSerializer

    def get_permissions(self):
        # разрешить пользователю, создавать с помощью POST
        return (permissions.AllowAny()
                if self.request.method == 'POST' else IsStaffOrTargetUser()),
