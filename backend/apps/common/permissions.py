from rest_framework import permissions


def get_active_memberships(user):
    if not user or not user.is_authenticated:
        return user.__class__.objects.none() if hasattr(user.__class__, "objects") else []
    return user.institute_memberships.filter(is_active=True).select_related(
        "institute",
        "class_darjah",
    )


def get_user_institute_ids(user):
    if not user or not user.is_authenticated:
        return []
    return list(get_active_memberships(user).values_list("institute_id", flat=True).distinct())


def get_primary_institute(user):
    if not user or not user.is_authenticated:
        return None
    if getattr(user, "institute_id", None):
        return user.institute
    membership = get_active_memberships(user).first()
    return membership.institute if membership else None


def has_institute_role(user, institute=None, roles=None):
    if not user or not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True

    roles = set(roles or [])
    memberships = get_active_memberships(user)
    if institute is not None:
        memberships = memberships.filter(institute=institute)
    if roles:
        memberships = memberships.filter(role__in=roles)
    return memberships.exists()


def can_access_institute(user, institute):
    if not institute:
        return False
    if not user or not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    if getattr(institute, "admin_id", None) == user.id:
        return True
    return has_institute_role(user, institute=institute)


def can_manage_institute(user, institute):
    if not institute:
        return False
    if not user or not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    if getattr(institute, "admin_id", None) == user.id:
        return True
    return has_institute_role(
        user,
        institute=institute,
        roles={"platform_admin", "institute_admin"},
    )


class IsAdmin(permissions.BasePermission):
    """Allow access only to platform admins."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsScholar(permissions.BasePermission):
    """Allow access only to verified scholars."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, 'scholar_profile', None)
        return bool(profile and profile.verification_status == 'verified')


class IsInstituteAdmin(permissions.BasePermission):
    """Allow access only to institute admins."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        institute = get_primary_institute(request.user)
        return can_manage_institute(request.user, institute)


class IsTeacher(permissions.BasePermission):
    """Allow access only to teachers."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return has_institute_role(request.user, roles={'teacher'})


class IsStudent(permissions.BasePermission):
    """Allow access only to students."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return has_institute_role(request.user, roles={'student'})


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

        if hasattr(obj, 'institute'):
            return has_institute_role(
                request.user,
                institute=obj.institute,
                roles={'platform_admin', 'institute_admin'},
            )
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
        profile = getattr(request.user, 'scholar_profile', None)
        if profile:
            return profile.verification_status == 'verified'
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


class IsPlatformAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))


class IsInstituteMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and get_active_memberships(request.user).exists())
