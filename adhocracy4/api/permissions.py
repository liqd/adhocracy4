from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or obj.project.has_moderator(request.user))


class IsCreatorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            obj.creator == request.user
            or request.user.is_superuser
            or obj.project.has_moderator(request.user))
