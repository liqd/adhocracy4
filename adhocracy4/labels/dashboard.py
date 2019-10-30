from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard import ModuleFormSetComponent
from adhocracy4.dashboard import components

from . import forms


class ModuleLabelsComponent(ModuleFormSetComponent):
    identifier = 'labels'
    weight = 14
    label = _('Labels')

    form_title = _('Edit labels')
    form_class = forms.LabelsFormSet
    form_template_name = 'a4labels/includes/module_labels_form.html'

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        for app, name in settings.A4_LABELS_ADDABLE:
            if app == module_app:
                return True
        return False


components.register_module(ModuleLabelsComponent())
