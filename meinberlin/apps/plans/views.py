import json

from django.conf import settings
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['items'] = json.dumps([{
            'title': item.title,
            'url': item.get_absolute_url(),
            'organisation': item.organisation.name,
            'point': item.point,
            'point_label': item.point_label,
            'cost': item.cost,
            'category': item.category,
            'status': item.status,
            'status_display': item.get_status_display(),
            'participation': item.participation,
            'participation_display': item.get_participation_display(),
        } for item in context['object_list']])

        context['baseurl'] = settings.A4_MAP_BASEURL
        context['attribution'] = settings.A4_MAP_ATTRIBUTION
        context['bounds'] = json.dumps(settings.A4_MAP_BOUNDING_BOX)

        return context
