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
        return models.Poll.objects.filter(module=self.module).first()


class ProjectManagementMixin(generic.base.ContextMixin):
    def dispatch(self, *args, **kwargs):
        # Based on adhocracy4.projects.mixins.ProjectMixin
        self.project = kwargs['project']
        self.module = self.project.module_set.first()
        self.request.module = self.module

        for arg in ['success_url', 'menu_item']:
            if hasattr(kwargs, arg):
                value = kwargs.pop(arg)
                setattr(self, arg, value)

        return super(ProjectManagementMixin, self).dispatch(*args, **kwargs)


class PollManagementView(ProjectManagementMixin,
                         rules_mixins.PermissionRequiredMixin,
                         generic.FormView):
    template_name = 'meinberlin_polls/poll_management_form.html'
    form_class = forms.PollForm
    permission_required = 'meinberlin_polls.create_poll'

    def get_success_url(self):
        # TODO: redirect to dashboard list
        return self.request.path
