from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.modules.models import Module
from adhocracy4.projects.mixins import DisplayProjectOrModuleMixin
from adhocracy4.projects.mixins import ProjectMixin

from . import forms
from . import models


class LiveQuestionModuleDetail(ProjectMixin,
                               generic.TemplateView,
                               DisplayProjectOrModuleMixin):
    template_name = 'meinberlin_livequestions/question_module_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['live_stream'] = \
            models.LiveStream.objects.filter(module=self.module).first()
        return context


class LiveQuestionPresentationListView(ProjectMixin,
                                       PermissionRequiredMixin,
                                       generic.ListView):

    model = models.LiveQuestion
    permission_required = 'meinberlin_livequestions.change_livequestion'

    def get_permission_object(self):
        return self.module

    def get_template_names(self):
        return ['meinberlin_livequestions/question_present_list.html']

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module)

    def get_full_url(self):
        request = self.request
        url = self.project.get_absolute_url()
        full_url = request.build_absolute_uri(url)
        return full_url


class LiveQuestionCreateView(PermissionRequiredMixin, generic.CreateView):
    model = models.LiveQuestion
    form_class = forms.LiveQuestionForm
    permission_required = 'meinberlin_livequestions.propose_livequestion'

    def dispatch(self, *args, **kwargs):
        mod_slug = self.kwargs[self.slug_url_kwarg]
        self.module = Module.objects.get(slug=mod_slug)
        self.project = self.module.project
        return super().dispatch(*args, **kwargs)

    def get_permission_object(self, *args, **kwargs):
        return self.module

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.module.slug
        context['project'] = self.project
        context['mode'] = 'create'
        return context

    def form_valid(self, form):
        self.request.session['user_category' + str(self.module.pk)] \
            = self.request.POST.get('category')
        form.instance.module = self.module
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['module'] = self.module
        if self.request.session.get('user_category' + str(self.module.pk)):
            kwargs['category_initial'] \
                = self.request.session.get('user_category'
                                           + str(self.module.pk))
        return kwargs


class LiveStreamDashboardView(ProjectMixin,
                              dashboard_mixins.DashboardBaseMixin,
                              dashboard_mixins.DashboardComponentMixin,
                              generic.UpdateView):
    model = models.LiveStream
    template_name = 'meinberlin_livequestions/livestream_dashboard_form.html'
    permission_required = 'a4projects.change_project'
    form_class = forms.LiveStreamForm

    def get_permission_object(self):
        return self.project

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.module = self.module
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return models.LiveStream.objects.filter(module=self.module).first()
