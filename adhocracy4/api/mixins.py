from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import clone_request
from rest_framework.response import Response

from adhocracy4.modules import models as module_models


class ContentTypeMixin:
    """
    Should be used in combination with ContentTypeRouter to fetch the
    decode content_type and object_pk of an request.

    Currently only numeric object_pk are supported.
    """
    content_type_filter = []

    def dispatch(self, request, *args, **kwargs):
        content_type = kwargs.get('content_type', '')
        object_pk = kwargs.get('object_pk', '')

        if not content_type.isdigit() or not object_pk.isdigit():
            raise Http404
        else:
            self.content_type_id = int(content_type)
            self.object_pk = int(object_pk)

        current_ct_strs = (
            self.content_type.app_label,
            self.content_type.model,
        )

        if current_ct_strs not in self.content_type_filter:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    @property
    def content_type(self):
        try:
            return ContentType.objects.get_for_id(self.content_type_id)
        except ContentType.DoesNotExist:
            raise Http404

    @property
    def content_object(self):
        return get_object_or_404(
            self.content_type.model_class(),
            pk=self.object_pk
        )


class ModuleMixin:
    """
    Should be used in combination with ModuleRouter to fetch the module.
    """

    def dispatch(self, request, *args, **kwargs):
        self.module_pk = kwargs.get('module_pk', '')
        return super().dispatch(request, *args, **kwargs)

    @property
    def module(self):
        return get_object_or_404(
            module_models.Module,
            pk=self.module_pk
        )


class OrganisationMixin:
    """
    Should be used in combination with OrganisationRouter to fetch the
    organisation.
    """

    def dispatch(self, request, *args, **kwargs):
        self.organisation_pk = kwargs.get('organisation_pk', '')
        return super().dispatch(request, *args, **kwargs)

    @property
    def organisation(self):
        return get_object_or_404(
            apps.get_model(settings.A4_ORGANISATIONS_MODEL),
            pk=self.organisation_pk
        )


class AllowPUTAsCreateMixin(object):
    """
    The following mixin class may be used in order to support PUT-as-create
    behavior for incoming requests.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup_value = self.kwargs[lookup_url_kwarg]
            extra_kwargs = {self.lookup_field: lookup_value}
            serializer.save(**extra_kwargs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                # xi: checks permission on wrong path
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise
