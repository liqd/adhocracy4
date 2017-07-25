from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import ProjectContextDispatcher
from meinberlin.apps.dashboard.mixins import DashboardBaseMixin

from . import models


class DocumentManagementView(ProjectContextDispatcher,
                             generic.TemplateView,
                             DashboardBaseMixin,
                             rules_mixins.PermissionRequiredMixin):
    template_name = 'meinberlin_documents/document_management.html'
    permission_required = 'a4projects.add_project'
    project_url_kwarg = 'slug'

    # Dashboard related attributes
    menu_item = 'project'

    def get_context_data(self, **kwargs):
        context = super(DocumentManagementView, self)\
            .get_context_data(**kwargs)
        # FIXME: Add multi-module support
        module = self.project.module_set.first()
        context['module'] = module
        return context


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
        return models.Chapter.objects.filter(
            module=self.project.last_active_module)


class DocumentDetailView(ChapterDetailView):

    def get_object(self):
        first_chapter = models.Chapter.objects \
            .filter(module=self.project.last_active_module) \
            .first()

        if not first_chapter:
            raise Http404(_('Document has no chapters defined.'))
        return first_chapter


class ParagraphDetailView(ProjectContextDispatcher,
                          rules_mixins.PermissionRequiredMixin,
                          generic.DetailView):
    model = models.Paragraph
    permission_required = 'meinberlin_documents.view_paragraph'
