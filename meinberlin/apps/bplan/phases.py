from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from adhocracy4 import phases
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins

from . import apps
from . import forms
from . import models


class BplanStatementFormView(
    ProjectMixin, rules_mixins.PermissionRequiredMixin, generic.CreateView
):
    model = models.Statement
    form_class = forms.StatementForm
    permission_required = "meinberlin_bplan.add_statement"
    template_name = "meinberlin_bplan/statement_create_form.html"
    success_url = reverse_lazy("meinberlin_bplan:statement-sent")

    def dispatch(self, request, *args, **kwargs):
        if self.project.has_finished:
            return HttpResponseRedirect(reverse("meinberlin_bplan:finished"))
        return super().dispatch(request, *args, **kwargs)

    def get_permission_object(self, *args, **kwargs):
        return self.module

    def form_valid(self, form):
        form.instance.module = self.module
        return super().form_valid(form)


class StatementPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = "statement"
    view = BplanStatementFormView

    name = _("Statement phase")
    description = _("Send statement to the office workers per mail.")
    module_name = _("bplan")

    features = {
        "crud": (models.Statement,),
    }


phases.content.register(StatementPhase())
