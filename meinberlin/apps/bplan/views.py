from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import ProjectContextDispatcher
from meinberlin.apps.dashboard2.components.forms.views import \
    ProjectComponentFormView
from meinberlin.apps.extprojects.views import ExternalProjectCreateView

from . import forms
from . import models


class BplanStatementFormView(ProjectContextDispatcher,
                             rules_mixins.PermissionRequiredMixin,
                             generic.CreateView):
    model = models.Statement
    form_class = forms.StatementForm
    permission_required = 'meinberlin_bplan.add_statement'
    template_name = 'meinberlin_bplan/statement_create_form.html'
    success_url = reverse_lazy('meinberlin_bplan:statement-sent')

    def get_permission_object(self, *args, **kwargs):
        return self.module

    def form_valid(self, form):
        form.instance.module = self.module
        return super().form_valid(form)


class BplanStatemenSentView(TemplateView):
    template_name = 'meinberlin_bplan/statement_sent.html'


class BplanProjectCreateView(ExternalProjectCreateView):

    model = models.Bplan
    slug_url_kwarg = 'project_slug'
    blueprint_key = 'bplan'
    form_class = forms.BplanProjectCreateForm
    template_name = 'meinberlin_dashboard/external_project_create_form.html'


class BplanProjectUpdateView(ProjectComponentFormView):

    model = models.Bplan

    def get_project(self, *args, **kwargs):
        project = super().get_project(*args, **kwargs)
        return project.externalproject.bplan

    def get_object(self, queryset=None):
        return self.project

    def validate_object_project(self):
        return True

    def validate_object_module(self):
        return True
