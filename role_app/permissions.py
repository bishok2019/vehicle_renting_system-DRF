from rest_framework.permissions import BasePermission
from.models import Permission

class IsSuperUser(BasePermission):
    """
    To check user is superuser or not
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

class HasPermission(BasePermission):
    """
    Custom permission class to check if a user has the required permission.
    """

    def has_permission(self, request, view):
        # Extract the required permission from the view
        required_permission = getattr(view, 'required_permission', None)

        if not request.user.is_authenticated:
            return False

        if not required_permission:
            return True # If no specific permission is required, allow access
        
        user_roles = request.user.role.all()
        user_permissions=set(Permission.objects.filter(roles__in=user_roles).values_list('code', flat=True))
        
        # code below optimized in single query above

        # for role in user_roles:
        # Checking if user has the required permission
            # user_permissions = set(Permission.objects.filter(roles__in=user_roles).values_list('code', flat=True))
            #This will be wrong because role and user are manytomanykey it can be usefull when accessing single object that is using foreign key
            # user_permissions = set(request.user.role.permissions.values_list('code', flat=True))
        
        return required_permission in user_permissions