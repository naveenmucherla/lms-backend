from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role.upper() == "ADMIN"
        )


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role.upper() == "MENTOR"
        )


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role.upper() == "STUDENT"
        )


class IsAdminOrMentor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role.upper() in ["ADMIN", "MENTOR"]
        )
