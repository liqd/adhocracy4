from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import models as category_models
from adhocracy4.dashboard.components.forms import ModuleDashboardFormSet
from adhocracy4.modules import models as module_models


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Category')}
    ))

    @property
    def media(self):
        media = super().media
        media.add_js(['js/formset.js'])
        return media

    class Meta:
        model = category_models.Category
        fields = ['name']


CategoryFormSet = inlineformset_factory(module_models.Module,
                                        category_models.Category,
                                        form=CategoryForm,
                                        formset=ModuleDashboardFormSet,
                                        extra=0,
                                        )
