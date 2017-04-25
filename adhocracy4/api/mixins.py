from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404

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
        self.module_slug = kwargs.get('module_slug', '')
        return super().dispatch(request, *args, **kwargs)

    @property
    def module(self):
        return get_object_or_404(
            module_models.Module,
            slug=self.module_slug
        )
