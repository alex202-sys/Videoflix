from rest_framework.permissions import BasePermission


class HasRefreshTokenCookie(BasePermission):
    """
    Allows access only if the refresh_token cookie is present.
    """

    message = "Refresh token missing."

    def has_permission(self, request, view):
        return bool(request.COOKIES.get("refresh_token"))
