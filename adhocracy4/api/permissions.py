from collections import namedtuple

from django.core.exceptions import PermissionDenied
from rest_framework import exceptions
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


RulesMethodMap = namedtuple('RulesMethodMap',
                            ['GET', 'OPTIONS', 'HEAD', 'POST',
                             'PUT', 'PATCH', 'DELETE'])


class RulesPermission(permissions.BasePermission):
    """
    Combining drf permissions with django-rules.
    """

    default_rules_method_map = RulesMethodMap(
        GET='{app_label}.view_{model_name}',
        OPTIONS='{app_label}.view_{model_name}',
        HEAD='{app_label}.view_{model_name}',
        POST='{app_label}.add_{model_name}',
        PUT='{app_label}.change_{model_name}',
        PATCH='{app_label}.change_{model_name}',
        DELETE='{app_label}.delete_{model_name}',
    )

    def get_rule(self, request, model_cls, method_map):
        template = getattr(method_map, request.method)

        if not template:
            raise exceptions.MethodNotAllowed(request.method)

        return template.format(
            app_label=model_cls._meta.app_label,
            model_name=model_cls._meta.model_name
        )

    def get_model_cls(self, request, view):
        queryset = view.get_queryset()
        return queryset.model

    def has_permission(self, request, view):
        """
        Check permission using get_permissions_object or get_object.

        By calling get_object to get an object for validation the rule
        has_object_permission will already be called. It maybe be called
        a third time if the handler also calls get_object. This is different
        from how drf/guardian integration handles this.
        """
        if hasattr(view, 'get_permission_object'):
            obj = view.get_permission_object()
        else:
            obj = view.get_object()

        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        if hasattr(view, 'rules_method_map'):
            rules_method_map = view.rules_method_map
        else:
            rules_method_map = self.default_rules_method_map

        model_cls = self.get_model_cls(request, view)
        perm = self.get_rule(request, model_cls, rules_method_map)

        if request.user.has_perm(perm, obj):
            return True

        raise PermissionDenied


class ViewSetRulesPermission(RulesPermission):
    non_object_actions = ['list', 'create']

    def has_permission(self, request, view):
        """
        Check permissions using get_object or get_permission_object depending
        on viewset action.
        """
        if not view.action or view.action in self.non_object_actions:
            obj = view.get_permission_object()
        else:
            obj = view.get_object()

        return self.has_object_permission(request, view, obj)
