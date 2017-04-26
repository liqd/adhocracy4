from django.views import generic

from adhocracy4.projects import mixins as project_mixins
from adhocracy4.rules import mixins as rules_mixins

from . import models


class DocumentCreateView(project_mixins.ProjectMixin, generic.TemplateView):
    template_name = 'meinberlin_documents/document_form.html'
    permission_required = 'meinberlin_documents.view'

    @property
    def document(self):
        return models.Document.objects.filter(module=self.module).first()


class DocumentDetailView(project_mixins.ProjectMixin, generic.DetailView):
    model = models.Document
    permission_required = 'meinberlin_documents.view_document'

    def get_object(self):
        return models.Document.objects.filter(module=self.module).first()


class ParagraphDetailView(rules_mixins.PermissionRequiredMixin,
                          generic.DetailView):
    model = models.Paragraph
    permission_required = 'meinberlin_documents.view_document'
