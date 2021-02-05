import json

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import CanonicalURLDetailView
from meinberlin.apps.maps.models import MapPreset
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.plans.forms import PlanForm
from meinberlin.apps.plans.models import Plan

from . import models


class PlanDetailView(rules_mixins.PermissionRequiredMixin,
                     CanonicalURLDetailView):
    model = models.Plan
    template_name = 'meinberlin_plans/plan_detail.html'
    permission_required = 'meinberlin_plans.view_plan'


class PlanListView(rules_mixins.PermissionRequiredMixin,
                   generic.ListView):
    model = models.Plan
    template_name = 'meinberlin_plans/plan_list.html'
    permission_required = 'meinberlin_plans.list_plan'

    def get_queryset(self):
        return super().get_queryset()\
            .select_related()

    @cached_property
    def districts(self):
        try:
            return MapPreset.objects.filter(
                category__name='Bezirke - Berlin')
        except ObjectDoesNotExist:
            return []

    def get_organisations(self):
        organisations = Organisation\
            .objects\
            .values_list('name', flat=True)\
            .order_by('name')
        return json.dumps(list(organisations))

    def get_district_polygons(self):
        districts = self.districts
        return json.dumps([district.polygon
                           for district in districts])

    def get_district_names(self):
        city_wide = _('City wide')
        districts = AdministrativeDistrict.objects.all()
        district_names_list = [district.name
                               for district in districts]
        district_names_list.append(str(city_wide))
        return json.dumps(district_names_list)

    def get_topics(self):
        topics = getattr(settings, 'A4_PROJECT_TOPICS', None)
        if topics:
            topic_dict = dict((x, str(y)) for x, y in topics)
            return json.dumps(topic_dict)
        else:
            raise ImproperlyConfigured('set A4_PROJECT_TOPICS in settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        use_vector_map = 0
        mapbox_token = ''
        omt_token = ''

        if (hasattr(settings, 'A4_USE_VECTORMAP') and
                settings.A4_USE_VECTORMAP):
            use_vector_map = 1

        if hasattr(settings, 'A4_MAPBOX_TOKEN'):
            mapbox_token = settings.A4_MAPBOX_TOKEN

        if hasattr(settings, 'A4_OPENMAPTILES_TOKEN'):
            omt_token = settings.A4_OPENMAPTILES_TOKEN

        context['districts'] = self.get_district_polygons()
        context['organisations'] = self.get_organisations()
        context['district_names'] = self.get_district_names()
        context['topic_choices'] = self.get_topics()
        context['containers_api_url'] = reverse('containers-list')
        context['extprojects_api_url'] = reverse('extprojects-list')
        context['privateprojects_api_url'] = reverse('privateprojects-list')
        context['projects_api_url'] = reverse('projects-list')
        context['plans_api_url'] = reverse('plans-list')
        context['baseurl'] = settings.A4_MAP_BASEURL
        context['mapbox_token'] = mapbox_token
        context['omt_token'] = omt_token
        context['use_vector_map'] = use_vector_map
        context['attribution'] = settings.A4_MAP_ATTRIBUTION
        context['bounds'] = json.dumps(settings.A4_MAP_BOUNDING_BOX)
        context['district'] = self.request.GET.get('district', -1)
        context['topic'] = self.request.GET.get('topic', -1)
        return context


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
    template_name = 'meinberlin_plans/plan_create_dashboard.html'
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
        return self.get_object()

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
        return self.get_object()

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})
