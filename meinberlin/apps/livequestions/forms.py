from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from adhocracy4.categories import forms as category_forms
from adhocracy4.categories import models as category_models
from adhocracy4.modules import models as module_models

from . import models


class LiveStreamForm(forms.ModelForm):
    class Meta:
        model = models.LiveStream
        fields = ['live_stream']


class AffiliationForm(category_forms.CategoryForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Affiliation')}
    ))


AffiliationFormSet = \
    inlineformset_factory(
        module_models.Module,
        category_models.Category,
        form=AffiliationForm,
        formset=category_forms.CategoryModuleDashboardFormSet,
        extra=0)
