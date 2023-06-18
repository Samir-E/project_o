from rest_framework import permissions


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # разрешить пользователю выводить список всех пользователей,
        # если вошедший в систему пользователь является сотрудником
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # разрешить вошедшему в систему пользователю
        # просматривать собственные данные,
        # позволяет сотрудникам просматривать все записи.
        return obj == request.user or request.user.is_staff

