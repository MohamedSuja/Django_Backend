# permissions.py
from rest_framework import permissions

class BaseRolePermission(permissions.BasePermission):
    allowed_roles = []
    
    def has_permission(self, request, view):
        if not hasattr(request, 'user_type'):
            return False
        return request.user_type in self.allowed_roles

class IsAdmin(BaseRolePermission):
    allowed_roles = ['admin']  # Already lowercase from middleware

class IsStaff(BaseRolePermission):
    allowed_roles = ['staff', 'admin']

class IsCustomer(BaseRolePermission):
    allowed_roles = ['customer']