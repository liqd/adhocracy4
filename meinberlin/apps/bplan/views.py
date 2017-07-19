from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import ProjectContextDispatcher

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
        return self.project.last_active_module

    def form_valid(self, form):
        form.instance.module = self.project.last_active_module
        return super().form_valid(form)


class BplanStatemenSentView(TemplateView):
    template_name = 'meinberlin_bplan/statement_sent.html'
