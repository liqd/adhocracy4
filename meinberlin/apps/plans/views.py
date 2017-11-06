from django.views import generic

from adhocracy4.rules import mixins as rules_mixins

from . import models


class PlanDetailView(rules_mixins.PermissionRequiredMixin,
                     generic.DetailView):
    model = models.Plan
    template_name = 'meinberlin_plans/plan_detail.html'
    permission_required = 'meinberlin_plans.view_plan'


class PlanListView(rules_mixins.PermissionRequiredMixin,
                   generic.ListView):
    model = models.Plan
    template_name = 'meinberlin_plans/plan_list.html'
    permission_required = 'meinberlin_plans.list_plan'
