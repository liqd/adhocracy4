from django.views import generic

from adhocracy4.projects import mixins as project_mixins
from adhocracy4.rules import mixins as rules_mixins

from . import models


class DocumentCreateView(project_mixins.ProjectMixin, generic.TemplateView):
    template_name = 'meinberlin_documents/chapter_form.html'
    permission_required = 'meinberlin_documents.change_chapter'

    @property
    def chapter(self):
        return models.Chapter.objects.filter(module=self.module).first()


class ChapterDetailView(project_mixins.ProjectMixin, generic.DetailView):
    model = models.Chapter
    permission_required = 'meinberlin_documents.view_chapter'

    def get_object(self):
        return models.Chapter.objects.filter(module=self.module).first()


class ParagraphDetailView(rules_mixins.PermissionRequiredMixin,
                          generic.DetailView):
    model = models.Paragraph
    permission_required = 'meinberlin_documents.view_chapter'
