from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_admin()

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_manager()

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_employee()

class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_admin() or request.user.is_manager())

class IsAdminOrEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_admin() or request.user.is_employee())