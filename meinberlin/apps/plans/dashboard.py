from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import ProjectFormComponent
from adhocracy4.dashboard import components

from . import forms


class PlanComponent(ProjectFormComponent):
    identifier = 'plans'
    weight = 33
    label = _('Plans')

    form_title = _('Edit Plan')
    form_class = forms.ProjectPlansDashboardForm
    form_template_name = 'meinberlin_plans/project_plans_form.html'


components.register_project(PlanComponent())
