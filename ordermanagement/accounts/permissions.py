from rest_framework.permissions import BasePermission, IsAuthenticated


class IsConsumer(BasePermission):
    """
        User permission set for views
    """

    def has_permission(self, request, view):
        user = request.user
        if str(user) != 'AnonymousUser':
            if user.is_consumer:
                return True
            else:
                return False
        else:
            return False
