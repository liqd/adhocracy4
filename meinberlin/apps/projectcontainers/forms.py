from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard.forms import ProjectCreateForm
from adhocracy4.dashboard.forms import ProjectDashboardForm
from adhocracy4.projects.enums import Access
from meinberlin.apps.contrib.widgets import Select2MultipleWidget

from . import models

LABELS = {
    'name': _('Title of your container'),
    'description': _('Short description of your container'),
    'tile_image': _('Logo'),
}

HELP_TEXTS = {
    'name': _('This title will appear on the '
              'teaser card and on top of the container '
              'detail page. It should be max. 120 characters long'),
    'description': _('This short description will appear on '
                     'the header of the container and in the teaser. '
                     'It should briefly state the goal of the '
                     'projects in max. 250 chars.'),
    'tile_image': _(
        'The image will be shown in the container tile.'
    ),
}


class ContainerCreateForm(ProjectCreateForm):

    class Meta:
        model = models.ProjectContainer
        fields = ['name', 'description',
                  'tile_image', 'tile_image_copyright']
        labels = LABELS
        help_texts = HELP_TEXTS


class ContainerBasicForm(ProjectDashboardForm):

    class Meta:
        model = models.ProjectContainer
        fields = ['name', 'description', 'tile_image',
                  'tile_image_copyright', 'is_archived']
        required_for_project_publish = ['name', 'description']
        labels = LABELS
        help_texts = HELP_TEXTS


class ContainerInformationForm(ProjectDashboardForm):

    class Meta:
        model = models.ProjectContainer
        fields = ['information']
        required_for_project_publish = ['information']
        labels = {
            'information': _('Description of your container'),
        }


class ContainerProjectsForm(ProjectDashboardForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.organisation = kwargs.pop('organisation')
        super().__init__(*args, **kwargs)

        projects = self.fields['projects']\
            .queryset.filter(organisation=self.organisation)
        if not self.organisation.has_initiator(self.user):
            user_groups = self.user.groups.all()
            org_groups = self.organisation.groups.all()
            shared_groups = user_groups & org_groups
            group = shared_groups.distinct().first()
            projects = projects.filter(group=group)

        self.fields['projects'].queryset = projects \
            .filter(projectcontainer=None)\
            .filter(Q(containers=self.instance) |
                    (Q(containers=None) &
                     Q(is_archived=False) &
                     Q(access=Access.PUBLIC) |
                     Q(access=Access.SEMIPUBLIC)))\
            .order_by('name')

    class Meta:
        model = models.ProjectContainer
        fields = ['projects']
        required_for_project_publish = ['projects']
        widgets = {
            'projects': Select2MultipleWidget,
        }
