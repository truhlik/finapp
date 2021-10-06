from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfileOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.id != obj.profile.user.id:
            return False
        return True


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return False
