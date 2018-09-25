from django import forms
from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard.components.forms import ProjectDashboardForm
from adhocracy4.maps import widgets as maps_widgets
from adhocracy4.projects import models as project_models
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
        fields = [
            'title',
            'description_image',
            'contact',
            'point',
            'point_label',
            'district',
            'cost',
            'description',
            'category',
            'status',
            'participation']
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].empty_label = _('City wide')


class CustomMultipleChoiceField(forms.ModelMultipleChoiceField):

    widget = forms.RadioSelect

    def clean(self, value):
        if value is None:
            return super().clean([])
        return super().clean([value])


class ProjectPlansDashboardForm(ProjectDashboardForm):
    plans = CustomMultipleChoiceField(queryset=None)

    class Meta:
        model = project_models.Project
        fields = ['plans']
        required_for_project_publish = ['plans']

    def save(self, commit=False):
        plans = self.cleaned_data['plans']
        self.instance.plans.set(plans)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['plans'] = self.instance.plans.all()
        self.fields['plans'
                    ].queryset = self.instance.organisation.plan_set.all()
