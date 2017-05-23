from django import forms

from adhocracy4.modules import forms as module_forms
from adhocracy4.categories import models as category_models


class CategorizableForm(module_forms.ItemForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = category_models.Category.objects.filter(module=self.module)
        self.fields['category'] = forms.ModelChoiceField(
            queryset=queryset,
            empty_label=None,
            required=False,
        )

    def show_categories(self):
        module_has_categories = len(self.fields['category'].queryset) > 0
        return module_has_categories
