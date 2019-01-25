import json

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from rest_framework.renderers import JSONRenderer

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.exports import mixins as export_mixins
from adhocracy4.exports import unescape_and_strip_html
from adhocracy4.exports import views as export_views
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import CanonicalURLDetailView
from meinberlin.apps.maps.models import MapPreset
from meinberlin.apps.plans.forms import PlanForm
from meinberlin.apps.plans.models import Plan
from meinberlin.apps.projects.models import Project

from . import models
from . import serializers


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

    def get_queryset(self):
        plans = super().get_queryset()\
            .select_related()
        return sorted(plans,
                      key=lambda x: x.modified or x.created,
                      reverse=True)

    @cached_property
    def districts(self):
        try:
            return MapPreset.objects.filter(
                category__name='Bezirke - Berlin')
        except ObjectDoesNotExist:
            return []

    @cached_property
    def projects(self):
        projects = Project.objects.all() \
            .filter(is_draft=False, is_archived=False) \
            .order_by('created')\
            .select_related('administrative_district',
                            'organisation',
                            'externalproject',
                            'projectcontainer')\
            .prefetch_related('moderators',
                              'organisation__initiators',
                              'module_set__phase_set')

        not_allowed_projects = [project.id for project in projects if
                                not self.request.user.has_perm(
                                    'a4projects.view_project',
                                    project)]
        return projects.exclude(id__in=not_allowed_projects)

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
        plans_serializer = serializers.PlanSerializer(context['object_list'],
                                                      many=True)
        projects_serializer = serializers.ProjectSerializer(self.projects,
                                                            many=True)
        items = plans_serializer.data + projects_serializer.data
        context['districts'] = self.get_district_polygons()
        context['district_names'] = self.get_district_names()
        context['topic_choices'] = self.get_topics()
        context['items'] = JSONRenderer().render(items)
        context['baseurl'] = settings.A4_MAP_BASEURL
        context['attribution'] = settings.A4_MAP_ATTRIBUTION
        context['bounds'] = json.dumps(settings.A4_MAP_BOUNDING_BOX)
        context['district'] = self.request.GET.get('district', -1)
        context['topic'] = self.request.GET.get('topic', -1)
        return context


class PlanExportView(rules_mixins.PermissionRequiredMixin,
                     export_mixins.ItemExportWithLinkMixin,
                     export_mixins.ExportModelFieldsMixin,
                     export_mixins.ItemExportWithLocationMixin,
                     export_views.BaseExport,
                     export_views.AbstractXlsxExportView):

    permission_required = 'meinberlin_plans.list_plan'
    model = models.Plan
    fields = ['title', 'organisation', 'contact', 'district', 'cost',
              'description', 'topics', 'status', 'participation']
    html_fields = ['description']

    def get_object_list(self):
        return models.Plan.objects.all()

    def get_base_filename(self):
        return 'plans_%s' % timezone.now().strftime('%Y%m%dT%H%M%S')

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual['projects'] = ugettext('Projects')
        virtual['projects_links'] = ugettext('Project Links')
        return virtual

    def get_organisation_data(self, item):
        return item.organisation.name

    def get_district_data(self, item):
        return item.district.name if item.district else str(_('City wide'))

    def get_contact_data(self, item):
        return unescape_and_strip_html(item.contact)

    def get_status_data(self, item):
        return item.get_status_display()

    def get_participation_data(self, item):
        return item.get_participation_display()

    def get_description_data(self, item):
        return unescape_and_strip_html(item.description)

    def get_projects_data(self, item):
        if item.projects.all():
            return ', \n'.join(
                [project.name
                 for project in item.projects.all()]
            )
        return ''

    def get_projects_links_data(self, item):
        if item.projects.all():
            return str([self.request.build_absolute_uri(
                        project.get_absolute_url())
                        for project in item.projects.all()
                        ])
        return ''


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
