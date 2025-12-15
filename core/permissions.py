from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permiso para administradores.
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated
            and hasattr(request.user, 'role')
            and request.user.role == 'admin'
        )


class IsOrganizer(BasePermission):
    """
    Permiso para organizadores.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'role')
            and request.user.role == 'organizer'
        )


class IsAttendee(BasePermission):
    """
    Permiso para asistentes.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'role')
            and request.user.role == 'attendee'
        )


class IsSponsor(BasePermission):
    """
    Permiso para patrocinadores.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'role')
            and request.user.role == 'sponsor'
        )