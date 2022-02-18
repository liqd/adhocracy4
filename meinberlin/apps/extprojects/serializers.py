from meinberlin.apps.extprojects.models import ExternalProject
from meinberlin.apps.projects.serializers import ProjectSerializer


class ExternalProjectSerializer(ProjectSerializer):

    class Meta:
        model = ExternalProject
        fields = ['type', 'subtype', 'title', 'url',
                  'organisation', 'tile_image',
                  'tile_image_copyright',
                  'point', 'point_label', 'cost',
                  'district', 'topics', 'access',
                  'status',
                  'participation_string',
                  'participation_active',
                  'participation', 'description',
                  'future_phase', 'active_phase',
                  'past_phase', 'plan_url', 'plan_title',
                  'published_projects_count', 'created_or_modified']

    def get_url(self, instance):
        return instance.externalproject.url

    def get_type(self, instance):
        return 'project'

    def get_subtype(self, instance):
        return 'external'

    def get_published_projects_count(self, instance):
        return 0
