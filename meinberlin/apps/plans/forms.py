from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from adhocracy4.maps import widgets as maps_widgets

from . import models


class PlanForm(forms.ModelForm):

    class Meta:
        model = models.Plan
        fields = ['title', 'contact', 'point', 'point_label', 'cost',
                  'description', 'category', 'status', 'participation',
                  'project']
        widgets = {
            'point': maps_widgets.MapChoosePointWidget(
                polygon=settings.BERLIN_POLYGON)
        }
        error_messages = {
            'point': {
                'required': _('Please locate the plan on the map.')
            }
        }
