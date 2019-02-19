from django.utils.translation import ugettext as _

from meinberlin.apps.extprojects.models import ExternalProject
from meinberlin.apps.projects.serializers import ProjectSerializer


class ExternalProjectSerializer(ProjectSerializer):

    class Meta:
        model = ExternalProject
        fields = ['type', 'subtype', 'title', 'url',
                  'organisation', 'tile_image',
                  'tile_image_copyright',
                  'point', 'point_label', 'cost',
                  'district', 'topics', 'is_public',
                  'status',
                  'participation_string',
                  'participation_active',
                  'participation', 'participation_display', 'description',
                  'future_phase', 'active_phase',
                  'past_phase', 'plan_url', 'plan_title',
                  'published_projects_count', 'created_or_modified']

    def _get_participation_status_project(self, instance):
        return _('done'), False

    def get_url(self, instance):
        return instance.externalproject.url

    def get_type(self, instance):
        return 'project'

    def get_subtype(self, instance):
        return 'external'

    def get_status(self, instance):
        return 1

    def get_future_phase(self, instance):
        return False

    def get_active_phase(self, instance):
        return False

    def get_past_phase(self, instance):
        return False

    def get_published_projects_count(self, instance):
        return 0
