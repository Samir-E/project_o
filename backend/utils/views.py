from rest_framework.serializers import Serializer


class ActionSerializerMixin:
    serializer_action_classes: dict[str, Serializer] = {}

    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value).

        Thanks gonz: http://stackoverflow.com/a/22922156/11440

        """
        action = self.action
        # Use the same serializer as for update as for partial update
        if 'update' in action:
            action = 'update'
        try:
            return self.serializer_action_classes[action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
