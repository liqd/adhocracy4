from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import ModuleFormSetComponent
from adhocracy4.dashboard import components

from . import forms


class ModerationTasksComponent(ModuleFormSetComponent):
    identifier = 'moderation_tasks'
    weight = 15
    label = _('Moderation Tasks')

    form_title = _('Edit moderation tasks')
    form_class = forms.ModerationTasksFormSet
    form_template_name = \
        'meinberlin_moderationtasks/moderation_tasks_form.html'

    def is_effective(self, module):
        return module.blueprint_type in ['PB1', 'PB2', 'PB3']


components.register_module(ModerationTasksComponent())
