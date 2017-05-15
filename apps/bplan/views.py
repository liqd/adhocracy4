from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from adhocracy4.rules import mixins as rules_mixins

from . import forms
from . import models


class BplanStatementFormView(rules_mixins.PermissionRequiredMixin,
                             generic.CreateView):
    model = models.Statement
    form_class = forms.StatementForm
    permission_required = 'meinberlin_bplan.add_statement'
    template_name = 'meinberlin_bplan/statement_create_form.html'
    success_url = reverse_lazy('meinberlin_bplan:statement-sent')

    def dispatch(self, *args, **kwargs):
        self.project = kwargs['project']
        self.phase = self.project.active_phase or self.project.past_phases[0]
        self.module = self.phase.module if self.phase else None
        return super(BplanStatementFormView, self).dispatch(*args, **kwargs)

    def get_permission_object(self, *args, **kwargs):
        return self.module

    def form_valid(self, form):
        form.instance.module = self.module
        return super().form_valid(form)


class BplanStatemenSentView(TemplateView):
    template_name = 'meinberlin_bplan/statement_sent.html'
