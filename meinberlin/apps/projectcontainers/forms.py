from meinberlin.apps.dashboard2.forms import ProjectDashboardForm

from . import models


class ContainerProjectForm(ProjectDashboardForm):

    class Meta:
        model = models.ProjectContainer
        fields = ['name', 'description', 'tile_image',
                  'tile_image_copyright', 'is_archived']
        required_for_project_publish = ['name', 'description']
