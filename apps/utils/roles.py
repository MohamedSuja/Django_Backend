from django.core.exceptions import PermissionDenied

def check_role_permission(user, required_permission):
    if not user.is_authenticated:
        raise PermissionDenied("Authentication required")
    
    if user.is_superuser:
        return True
    
    try:
        user_role = user.role
        if required_permission in user_role.permissions:
            return True
    except AttributeError:
        pass
    
    raise PermissionDenied("You don't have permission to perform this action")