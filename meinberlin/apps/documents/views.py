from django.http import Http404
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import ProjectContextDispatcher
from meinberlin.apps.dashboard2 import mixins as dashboard_mixins
from meinberlin.apps.exports import views as export_views

from . import models


class DocumentDashboardView(dashboard_mixins.DashboardComponentMixin,
                            dashboard_mixins.DashboardBaseMixin,
                            dashboard_mixins.DashboardContextMixin,
                            generic.TemplateView):
    template_name = 'meinberlin_documents/document_dashboard.html'
    permission_required = 'a4projects.add_project'


class ChapterDetailView(ProjectContextDispatcher,
                        rules_mixins.PermissionRequiredMixin,
                        generic.DetailView):
    model = models.Chapter
    permission_required = 'meinberlin_documents.view_chapter'

    def get_context_data(self, **kwargs):
        context = super(ChapterDetailView, self).get_context_data(**kwargs)
        context['chapter_list'] = self.chapter_list
        return context

    @property
    def chapter_list(self):
        return models.Chapter.objects.filter(module=self.module)


class DocumentExportView(export_views.AbstractXlsxExportView,
                         export_views.ItemExportWithCommentsMixin):

    PARAGRAPH_TEXT_LIMIT = 100

    def get_header(self):
        return map(str, [_('Chapter'), _('Paragraph'), _('Comments')])

    def export_rows(self):
        chapters = models.Chapter.objects.filter(module=self.module)

        for chapter in chapters:
            yield [chapter.name, '', self.get_comments_data(chapter)]
            for paragraph in chapter.paragraphs.all():
                yield [chapter.name,
                       self.get_paragraph_data(paragraph),
                       self.get_comments_data(paragraph)]

    def get_paragraph_data(self, paragraph):
        if paragraph.name:
            return paragraph.name

        text = strip_tags(paragraph.text).strip()
        return text[0:self.PARAGRAPH_TEXT_LIMIT] + ' ...'


class DocumentDetailView(ChapterDetailView):
    exports = [(_('Documents with comments'), DocumentExportView)]

    def get_object(self):
        first_chapter = models.Chapter.objects \
            .filter(module=self.module) \
            .first()

        if not first_chapter:
            raise Http404(_('Document has no chapters defined.'))
        return first_chapter


class ParagraphDetailView(ProjectContextDispatcher,
                          rules_mixins.PermissionRequiredMixin,
                          generic.DetailView):
    model = models.Paragraph
    permission_required = 'meinberlin_documents.view_paragraph'
