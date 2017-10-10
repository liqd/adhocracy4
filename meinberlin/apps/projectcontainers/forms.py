from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.dashboard2.forms import ProjectCreateForm
from meinberlin.apps.dashboard2.forms import ProjectDashboardForm

from . import models


class ContainerCreateForm(ProjectCreateForm):

    class Meta:
        model = models.ProjectContainer
        fields = ['name', 'description',
                  'tile_image', 'tile_image_copyright']

        labels = {
            'name': _('Title of your container'),
            'description': _('Short description of your container'),
        }
        help_texts = {
            'name': _('This title will appear on the '
                      'teaser card and on top of the container '
                      'detail page. It should be max. 120 characters long'),
            'description': _('This short description will appear on '
                             'the header of the container and in the teaser. '
                             'It should briefly state the goal of the '
                             'projects in max. 250 chars.')
        }


class ContainerProjectForm(ProjectDashboardForm):

    class Meta:
        model = models.ProjectContainer
        fields = ['name', 'description', 'tile_image',
                  'tile_image_copyright', 'is_archived']
        required_for_project_publish = ['name', 'description']
