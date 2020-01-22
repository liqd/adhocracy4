from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard.components.forms import ModuleDashboardFormSet
from adhocracy4.labels import models as labels_models
from adhocracy4.modules import models as module_models


class LabelForm(forms.ModelForm):
    def __init__(self, module, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Category name')

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Label')}
    ))

    class Media:
        js = ('category_formset.js',)

    class Meta:
        model = labels_models.Label
        fields = ['name']


class LabelModuleDashboardFormSet(ModuleDashboardFormSet):
    def get_form_kwargs(self, index):
        form_kwargs = super().get_form_kwargs(index)
        form_kwargs['module'] = self.instance
        return form_kwargs


LabelsFormSet = inlineformset_factory(module_models.Module,
                                      labels_models.Label,
                                      form=LabelForm,
                                      formset=LabelModuleDashboardFormSet,
                                      extra=0)
