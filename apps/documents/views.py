from django.views import generic

from adhocracy4.modules import views as module_views
from adhocracy4.rules import mixins as rules_mixins

from . import models


class DocumentCreateView(module_views.ItemCreateView):
    template_name = 'meinberlin_documents/document_form.html'
    permission_required = 'meinberlin_documents.view'

    @property
    def document(self):
        return models.Document.objects.filter(module=self.module).first()


class DocumentDetailView(module_views.ItemDetailView):
    model = models.Document
    permission_required = 'meinberlin_documents.view'

    def get_object(self):
        return models.Document.objects.filter(module=self.module).first()


class ParagraphDetailView(rules_mixins.PermissionRequiredMixin,
                          generic.DetailView):
    model = models.Paragraph
    permission_required = 'meinberlin_documents.view'
