from django.http import Http404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib import mixins as contrib_mixins
from meinberlin.apps.exports.views import DashboardExportView

from . import models


class DocumentDashboardView(ProjectMixin,
                            dashboard_mixins.DashboardBaseMixin,
                            dashboard_mixins.DashboardComponentMixin,
                            generic.TemplateView):
    template_name = 'meinberlin_documents/document_dashboard.html'
    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.project


class ChapterDetailView(ProjectMixin,
                        rules_mixins.PermissionRequiredMixin,
                        generic.DetailView,
                        contrib_mixins.DisplayProjectOrModuleMixin):
    model = models.Chapter
    permission_required = 'meinberlin_documents.view_chapter'
    get_context_from_object = True

    def get_context_data(self, **kwargs):
        context = super(ChapterDetailView, self).get_context_data(**kwargs)
        context['chapter_list'] = self.chapter_list
        return context

    @property
    def chapter_list(self):
        return models.Chapter.objects.filter(module=self.module)


class DocumentDetailView(ChapterDetailView):
    get_context_from_object = False

    def get_object(self):
        first_chapter = models.Chapter.objects \
            .filter(module=self.module) \
            .first()

        if not first_chapter:
            raise Http404(_('Document has no chapters defined.'))
        return first_chapter


class ParagraphDetailView(ProjectMixin,
                          rules_mixins.PermissionRequiredMixin,
                          generic.DetailView):
    model = models.Paragraph
    permission_required = 'meinberlin_documents.view_paragraph'


class DocumentDashboardExportView(DashboardExportView):
    template_name = 'meinberlin_exports/export_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_export'] = reverse(
            'a4dashboard:document-comment-export',
            kwargs={'module_slug': self.module.slug})
        return context
