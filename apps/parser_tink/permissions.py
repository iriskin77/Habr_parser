from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return True
        else:
            return bool(request.user and request.user.is_staff)


class IsAdminOrReadPostOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in ('GET', 'POST', 'OPTIONS', 'HEAD'):
            return True
        else:
            return bool(request.user and request.user.is_staff)
