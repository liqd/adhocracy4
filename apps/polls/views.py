from django.views import generic

from adhocracy4.projects import mixins as project_mixins
from adhocracy4.rules import mixins as rules_mixins

from . import forms
from . import models


class PollDetailView(project_mixins.ProjectMixin,
                     rules_mixins.PermissionRequiredMixin,
                     generic.DetailView):
    model = models.Poll
    permission_required = 'meinberlin_polls.view_poll'

    def get_object(self):
        return models.Poll.filter(module=self.module).first()


class PollCreateView(project_mixins.ProjectMixin,
                     rules_mixins.PermissionRequiredMixin,
                     generic.FormView):
    template_name = 'meinberlin_polls/poll_form.html'
    form_class = forms.PollForm
    permission_required = 'meinberlin_polls.view_poll'

    def get_success_url(self):
        return self.request.path
