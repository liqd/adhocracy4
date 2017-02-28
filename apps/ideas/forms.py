from django import forms

from adhocracy4.categories import models as category_models

from . import models


class IdeaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        module = kwargs.pop('module')
        super().__init__(*args, **kwargs)
        queryset = category_models.Category.objects.filter(module=module)
        self.fields['category'] = forms.ModelChoiceField(
            queryset=queryset,
            empty_label=None,
            required=False,
        )

    def show_categories(self):
        module_has_categories = len(self.fields['category'].queryset) > 0
        return module_has_categories

    class Meta:
        model = models.Idea
        fields = ['name', 'description', 'category']
