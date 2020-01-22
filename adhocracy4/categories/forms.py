from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import models as category_models
from adhocracy4.dashboard.components.forms import ModuleDashboardFormSet
from adhocracy4.modules import models as module_models

from . import has_icons


class CategorizableFieldMixin:
    category_field_name = 'category'

    def __init__(self, *args, **kwargs):
        self.module = kwargs.pop('module')
        super().__init__(*args, **kwargs)

        field = self.fields[self.category_field_name]
        field.queryset = category_models.Category.objects.filter(
            module=self.module)

        required = field.queryset.exists()
        field.empty_label = None
        field.required = required
        field.widget.is_required = required

    def show_categories(self):
        field = self.fields[self.category_field_name]
        module_has_categories = field.queryset.exists()
        return module_has_categories


class CategoryForm(forms.ModelForm):
    def __init__(self, module, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Category name')
        self.fields['icon'].label = _('Category icon')

        if not (module and has_icons(module)):
            del self.fields['icon']

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Category')}
    ))

    class Media:
        js = ('category_formset.js',)

    class Meta:
        model = category_models.Category
        fields = ['name', 'icon']


class CategoryModuleDashboardFormSet(ModuleDashboardFormSet):
    def get_form_kwargs(self, index):
        form_kwargs = super().get_form_kwargs(index)
        form_kwargs['module'] = self.instance
        return form_kwargs


CategoryFormSet = inlineformset_factory(module_models.Module,
                                        category_models.Category,
                                        form=CategoryForm,
                                        formset=CategoryModuleDashboardFormSet,
                                        extra=0,
                                        )
