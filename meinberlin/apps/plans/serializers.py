from functools import lru_cache

from rest_framework import serializers

from meinberlin.apps.projects.serializers import CommonFields

from .models import Plan


class PlanSerializer(serializers.ModelSerializer, CommonFields):
    type = serializers.SerializerMethodField()
    subtype = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    published_projects_count = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    created_or_modified = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['type', 'subtype', 'title', 'url',
                  'organisation', 'point',
                  'point_label', 'cost',
                  'district', 'topics', 'status',
                  'participation',
                  'participation_string',
                  'participation_active',
                  'published_projects_count', 'created_or_modified']

    def get_subtype(self, instance):
        return 'plan'

    @lru_cache(maxsize=1)
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
        participation_string, participation_active = \
            self._get_participation_status_plan(instance)
        return str(participation_string)

    def get_participation_active(self, instance):
        participation_string, participation_active = \
            self._get_participation_status_plan(instance)
        return participation_active
