from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard.components.forms import ModuleDashboardFormSet
from adhocracy4.modules import models as module_models

from .models import ModerationTask


class ModerationTaskForm(forms.ModelForm):
    def __init__(self, module, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = _("Moderation task")

    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Moderation tasks")})
    )

    class Media:
        js = ("category_formset.js",)

    class Meta:
        model = ModerationTask
        fields = ["name"]


class ModerationTaskModuleDashboardFormSet(ModuleDashboardFormSet):
    def get_form_kwargs(self, index):
        form_kwargs = super().get_form_kwargs(index)
        form_kwargs["module"] = self.instance
        return form_kwargs


ModerationTasksFormSet = inlineformset_factory(
    module_models.Module,
    ModerationTask,
    form=ModerationTaskForm,
    formset=ModerationTaskModuleDashboardFormSet,
    extra=0,
)
