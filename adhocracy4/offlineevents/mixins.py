from django.forms import modelformset_factory
from django.views.generic.base import ContextMixin

from .forms import OfflineEventDocumentForm
from .models import OfflineEventDocument


class OfflineEventFormMixin(ContextMixin):

    def empty_upload_formset(self):
        queryset = OfflineEventDocument.objects.none()
        return modelformset_factory(
            OfflineEventDocument,
            OfflineEventDocumentForm,
            extra=1, max_num=5, can_delete=True)(queryset=queryset)

    def update_upload_formset(self, queryset):
        return modelformset_factory(
            OfflineEventDocument,
            OfflineEventDocumentForm,
            extra=1, max_num=5, can_delete=True)(queryset=queryset)

    def filled_upload_formset(self, request):
        return modelformset_factory(
            OfflineEventDocument,
            OfflineEventDocumentForm,
            extra=1, max_num=5, can_delete=True)(request.POST, request.FILES)

    def get_context_data(self, **kwargs):
        field = OfflineEventDocument._meta.get_field('document')
        kwargs['max_size_mb'] = field.max_size_mb
        kwargs['allowed_file_types'] = field.allowed_file_types
        return super().get_context_data(**kwargs)
