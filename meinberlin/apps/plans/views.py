import json

from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import CanonicalURLDetailView
from meinberlin.apps.dashboard2 import mixins as a4dashboard_mixins
from meinberlin.apps.exports import views as export_views
from meinberlin.apps.plans.forms import PlanForm
from meinberlin.apps.plans.models import Plan

from . import models


class PlanDetailView(rules_mixins.PermissionRequiredMixin,
                     CanonicalURLDetailView):
    model = models.Plan
    template_name = 'meinberlin_plans/plan_detail.html'
    permission_required = 'meinberlin_plans.view_plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['berlin_polygon'] = settings.BERLIN_POLYGON
        return context


class PlanListView(rules_mixins.PermissionRequiredMixin,
                   generic.ListView):
    model = models.Plan
    template_name = 'meinberlin_plans/plan_list.html'
    permission_required = 'meinberlin_plans.list_plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items = sorted(context['object_list'],
                       key=lambda x: x.modified or x.created,
                       reverse=True)

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
        } for item in items])

        context['baseurl'] = settings.A4_MAP_BASEURL
        context['attribution'] = settings.A4_MAP_ATTRIBUTION
        context['bounds'] = json.dumps(settings.A4_MAP_BOUNDING_BOX)

        return context


class PlanExportView(rules_mixins.PermissionRequiredMixin,
                     export_views.ItemExportWithLocationMixin,
                     export_views.ItemExportView):

    permission_required = 'meinberlin_plans.list_plan'
    model = models.Plan
    fields = ['title', 'organisation', 'project', 'contact', 'cost',
              'description', 'category', 'status', 'participation']

    def get_queryset(self):
        return models.Plan.objects.all()

    def get_base_filename(self):
        return 'plans_%s' % timezone.now().strftime('%Y%m%dT%H%M%S')

    def get_organisation_data(self, item):
        return item.organisation.name

    def get_project_data(self, item):
        if item.project:
            return item.project.name
        return ''

    def get_contact_data(self, item):
        return strip_tags(item.contact).strip()


class DashboardPlanListView(a4dashboard_mixins.DashboardBaseMixin,
                            generic.ListView):
    model = Plan
    template_name = 'meinberlin_plans/plan_dashboard_list.html'
    permission_required = 'meinberlin_plans.add_plan'
    menu_item = 'project'

    def get_permission_object(self):
        return self.organisation

    def get_queryset(self):
        return super().get_queryset().filter(organisation=self.organisation)


class DashboardPlanCreateView(a4dashboard_mixins.DashboardBaseMixin,
                              generic.CreateView):
    model = Plan
    form_class = PlanForm
    permission_required = 'meinberlin_plans.add_plan'
    template_name = 'meinberlin_plans/plan_create_form.html'
    menu_item = 'project'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.organisation = self.organisation
        return super().form_valid(form)

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})


class DashboardPlanUpdateView(a4dashboard_mixins.DashboardBaseMixin,
                              generic.UpdateView):
    model = Plan
    form_class = PlanForm
    permission_required = 'meinberlin_plans.change_plan'
    template_name = 'meinberlin_plans/plan_update_form.html'
    menu_item = 'project'

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})


class DashboardPlanDeleteView(a4dashboard_mixins.DashboardBaseMixin,
                              generic.DeleteView):
    model = Plan
    success_message = _('The plan has been deleted')
    permission_required = 'meinberlin_plans.change_plan'
    template_name = 'meinberlin_plans/plan_confirm_delete.html'
    menu_item = 'project'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})
