from rest_framework.permissions import BasePermission
from .models import UserAccount


class HasAccountPermission(BasePermission):

    def has_permission(self, request, view):

        # Check the permissions for the other paths
        account_id = view.kwargs.get('account_id')
        if not account_id:
            return False

        try:
            user_permission = UserAccount.objects.get(user_account=request.user, investment_account_id=account_id)
        except UserAccount.DoesNotExist:
            return False

        if request.method == 'GET' and user_permission.permissions in [UserAccount.VIEW_ONLY, UserAccount.FULL_CRUD]:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE'] and user_permission.permissions == UserAccount.FULL_CRUD:
            return True
        elif request.method == 'POST' and user_permission.permissions == UserAccount.POST_ONLY:
            return True

        return False


class UserViewPermission(BasePermission):

    def has_permission(self, request, view):
        # Allow access to POST requests for Users without authentication
        if request.method == 'POST' and request.path == '/api/users/':
            return True
        return request.user and request.user.is_authenticated
