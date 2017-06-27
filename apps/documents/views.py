from django.views import generic

from adhocracy4.modules import views as module_views
from adhocracy4.projects.views import ProjectContextDispatcher
from adhocracy4.rules import mixins as rules_mixins
from apps.dashboard.mixins import DashboardBaseMixin

from . import models


class DocumentManagementView(generic.TemplateView,
                             DashboardBaseMixin,
                             rules_mixins.PermissionRequiredMixin):
    template_name = 'meinberlin_documents/document_management.html'
    permission_required = 'a4projects.add_project'

    # Dashboard related attributes
    menu_item = 'project'

    def dispatch(self, *args, **kwargs):
        self.project = kwargs['project']
        self.module = self.project.modules.first()
        self.request.module = self.module

        return super(DocumentManagementView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DocumentManagementView, self)\
            .get_context_data(**kwargs)
        context['module'] = self.module
        return context


class ChapterManagementView(module_views.ItemDetailView):
    model = models.Chapter
    template_name = 'meinberlin_documents/chapter_form.html'
    permission_required = 'meinberlin_documents.change_chapter'

    @property
    def module(self):
        return self.get_object().module

    @property
    def project(self):
        return self.get_object().project

    @property
    def organisation(self):
        return self.get_object().project.organisation


class ChapterDetailView(rules_mixins.PermissionRequiredMixin,
                        generic.DetailView):
    model = models.Chapter
    permission_required = 'meinberlin_documents.view_chapter'

    def get_context_data(self, **kwargs):
        context = super(ChapterDetailView, self).get_context_data(**kwargs)
        context['chapter_list'] = self.chapter_list
        return context

    def dispatch(self, *args, **kwargs):
        chapter = self.get_object()

        # Simulate ProjectMixin behaviour
        self.project = chapter.project
        self.phase = self.project.active_phase \
            or self.project.past_phases.first()
        self.module = chapter.module
        self.request.module = self.module

        return super(ChapterDetailView, self).dispatch(*args, **kwargs)

    @property
    def chapter_list(self):
        return models.Chapter.objects.filter(module=self.module)


class DocumentDetailView(ProjectContextDispatcher, ChapterDetailView):
    def get_object(self):
        return models.Chapter.objects\
            .filter(module=self.project.active_module)\
            .first()


class ParagraphDetailView(rules_mixins.PermissionRequiredMixin,
                          generic.DetailView):
    model = models.Paragraph
    permission_required = 'meinberlin_documents.view_paragraph'
