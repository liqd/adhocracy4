from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.projects import mixins

from . import models


class DocumentCreateView(mixins.ProjectMixin, generic.TemplateView):
    template_name = 'meinberlin_documents/document_form.html'
    permission_required = 'meinberlin_documents.view'

    @property
    def document(self):
        return models.Document.objects.filter(module=self.module).first()


class DocumentDetailView(generic.DetailView, mixins.ProjectMixin):
    model = models.Document
    permission_required = 'meinberlin_documents.view'

    def get_object(self):
        return models.Document.objects.filter(module=self.module).first()


class ParagraphDetailView(PermissionRequiredMixin, generic.DetailView):
    model = models.Paragraph
    permission_required = 'meinberlin_documents.view'

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated()
