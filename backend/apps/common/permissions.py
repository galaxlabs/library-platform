from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class IsAdmin(permissions.BasePermission):
    """Allow access only to platform admins."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsScholar(permissions.BasePermission):
    """Allow access only to verified scholars."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'scholar') and request.user.scholar.verification_status == 'verified'


class IsInstituteAdmin(permissions.BasePermission):
    """Allow access only to institute admins."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.institute and request.user.roles.filter(name='Institute Admin').exists()


class IsTeacher(permissions.BasePermission):
    """Allow access only to teachers."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.roles.filter(name='Teacher').exists()


class IsStudent(permissions.BasePermission):
    """Allow access only to students."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.roles.filter(name='Student').exists()


class IsInstituteAdminOrReadOnly(permissions.BasePermission):
    """
    Allow institute admins to edit their institute's data.
    Allow read-only access to authenticated users.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read permission for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permission only for institute admins of that institute
        if hasattr(obj, 'institute'):
            return obj.institute == request.user.institute
        return False


class IsScholarOrReadOnly(permissions.BasePermission):
    """
    Allow scholars to create/update reviews.
    Allow read-only access to all authenticated users.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read permission for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permission for scholars
        if hasattr(request.user, 'scholar'):
            return request.user.scholar.verification_status == 'verified'
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow users to edit their own objects.
    Allow read-only access to others.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permission for all
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write only if owner
        return obj.user == request.user