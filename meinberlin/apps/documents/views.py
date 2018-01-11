from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.dashboard2 import mixins as dashboard_mixins

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
                        generic.DetailView):
    model = models.Chapter
    permission_required = 'meinberlin_documents.view_chapter'
    get_context_from_object = True

    def dispatch(self, request, *args, **kwargs):
        # Redirect first chapter view to the project detail page
        res = super().dispatch(request, *args, **kwargs)
        chapter = self.get_object()
        if self.request.path == chapter.get_absolute_url() \
                and chapter == self.chapter_list.first():
            return HttpResponseRedirect(self.project.get_absolute_url())
        else:
            return res

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
