from django import forms
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.bplan import models as bplan_models
from meinberlin.apps.extprojects.forms import ExternalProjectCreateForm
from meinberlin.apps.extprojects.forms import ExternalProjectForm
from meinberlin.apps.organisations.models import Organisation


class OrganisationForm(forms.ModelForm):

    class Meta:
        model = Organisation
        fields = ['name', 'logo']
        labels = {
            'name': _('Organisation name')
        }


class BplanProjectCreateForm(ExternalProjectCreateForm):

    class Meta:
        model = bplan_models.Bplan
        fields = ['name', 'description', 'tile_image', 'tile_image_copyright']


class BplanProjectForm(ExternalProjectForm):

    class Meta:
        model = bplan_models.Bplan
        fields = ['name', 'url', 'description', 'tile_image',
                  'tile_image_copyright', 'is_archived', 'office_worker_email']
        required_for_project_publish = ['name', 'url', 'description',
                                        'office_worker_email']
