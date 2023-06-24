from rest_framework import serializers

from .models import BookFeedback


class BookFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookFeedback
        fields = "__all__"
