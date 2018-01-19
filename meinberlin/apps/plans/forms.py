from django import forms
from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from adhocracy4.maps import widgets as maps_widgets
from meinberlin.apps.contrib import widgets as contrib_widgets

from . import models


def get_category_options():
    return models.Plan.objects\
        .filter(~Q(category=''))\
        .order_by('category')\
        .values_list('category', flat=True)\
        .distinct()


class PlanForm(forms.ModelForm):

    class Meta:
        model = models.Plan
        fields = ['title', 'contact', 'point', 'point_label', 'district',
                  'cost', 'description', 'category', 'status',
                  'participation', 'project']
        widgets = {
            'point': maps_widgets.MapChoosePointWidget(
                polygon=settings.BERLIN_POLYGON),
            'category': contrib_widgets.TextWithDatalistWidget(attrs={
                'options': get_category_options
            })
        }
        error_messages = {
            'point': {
                'required': _('Please locate the plan on the map.')
            }
        }
