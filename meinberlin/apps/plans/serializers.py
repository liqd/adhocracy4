from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project
from meinberlin.apps.projects import get_project_type

from .models import Plan


class CommonFields:

    def get_district(self, instance):
        city_wide = _('City wide')
        district_name = str(city_wide)
        if instance.administrative_district:
            district_name = instance.administrative_district.name
        return district_name

    def get_point(self, instance):
        point = instance.point
        if not point:
            point = ''
        return point


class ProjectSerializer(serializers.ModelSerializer, CommonFields):
    type = serializers.SerializerMethodField()
    subtype = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    future_phase = serializers.SerializerMethodField()
    active_phase = serializers.SerializerMethodField()
    past_phase = serializers.SerializerMethodField()
    tile_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['type', 'subtype', 'title', 'url',
                  'tile_image', 'tile_image_copyright',
                  'point', 'district', 'topic',
                  'status', 'participation_string',
                  'participation_active',
                  'description', 'future_phase',
                  'active_phase',
                  'past_phase']

    @cached_property
    def phases(self):
        return Phase.objects\
            .select_related('module__project')

    def _get_phases_for_instance(self, instance):
        return self.phases.filter(
            module__project_id__in=[instance.id])

    def _get_participation_status_project(self, instance):
        project_phases = self._get_phases_for_instance(instance)

        if project_phases.active_phases():
            return _('running'), True

        if project_phases.future_phases():
            try:
                return (_('starts at {}').format
                        (project_phases.future_phases().first().
                         start_date.date()),
                        True)
            except AttributeError:
                return (_('starts in the future'),
                        True)
        else:
            return _('done'), False

    def get_type(self, instance):
        return 'project'

    def get_subtype(self, instance):
        subtype = get_project_type(instance)
        if subtype in ('external', 'bplan'):
            return 'external'
        return subtype

    def get_title(self, instance):
        return instance.name

    def get_url(self, instance):
        if get_project_type(instance) in ('external', 'bplan'):
            return instance.externalproject.url
        return instance.get_absolute_url()

    def get_tile_image(self, instance):
        image_url = ''
        if instance.tile_image:
            image = get_thumbnailer(instance.tile_image)['project_tile']
            image_url = image.url
        return image_url

    def get_status(self, instance):
        project_phases = \
            self.phases.filter(
                module__project_id__in=[instance.id])
        if project_phases.active_phases() or project_phases.future_phases():
            return 2
        return 3

    def get_future_phase(self, instance):
        if (instance.future_phases and
                instance.future_phases.first().start_date):
            return str(
                instance.future_phases.first().start_date.date())
        return False

    def get_active_phase(self, instance):
        project_phases = self._get_phases_for_instance(instance)
        if project_phases.active_phases():
            progress = instance.active_phase_progress
            time_left = instance.time_left
            return [progress, time_left]
        return False

    def get_past_phase(self, instance):
        project_phases = self._get_phases_for_instance(instance)
        if project_phases.past_phases():
            return True
        return False

    def get_participation_string(self, instance):
        participation_string, active = \
            self._get_participation_status_project(instance)
        return str(participation_string)

    def get_participation_active(self, instance):
        participation_string, active = \
            self._get_participation_status_project(instance)
        return active


class PlanSerializer(serializers.ModelSerializer, CommonFields):
    type = serializers.SerializerMethodField()
    subtype = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    published_projects_count = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['type', 'subtype', 'title', 'url',
                  'point', 'district', 'topic', 'status',
                  'participation_string',
                  'participation_active',
                  'published_projects_count']

    def get_subtype(self, instance):
        return 'plan'

    def _get_participation_status_plan(self, item):
        projects = item.published_projects
        if not projects:
            return item.get_participation_display(), False
        else:
            status_string = item.participation_string
            if status_string:
                return status_string, True
            else:
                return item.get_participation_display(), False

    def get_type(self, instance):
        return 'plan'

    def get_url(self, instance):
        return instance.get_absolute_url()

    def get_published_projects_count(self, instance):
        return instance.published_projects.count()

    def get_participation_string(self, instance):
        participation_string, active = \
            self._get_participation_status_plan(instance)
        return str(participation_string)

    def get_participation_active(self, instance):
        participation_string, active = \
            self._get_participation_status_plan(instance)
        return active
