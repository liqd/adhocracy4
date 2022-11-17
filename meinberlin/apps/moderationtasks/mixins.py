from adhocracy4.forms import widgets
from meinberlin.apps.moderationtasks.models import ModerationTask


class TasksAddableFieldMixin:
    tasks_field_name = 'completed_tasks'

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'module'):
            self.module = kwargs['instance'].module
        super().__init__(*args, **kwargs)

        field = self.fields[self.tasks_field_name]
        field.queryset = ModerationTask.objects.filter(module=self.module)
        field.required = False
        field.widget = widgets.CustomCheckboxSelectMultiple(
            choices=[(task.id, task.name) for task in field.queryset])

    def show_tasks(self):
        field = self.fields[self.tasks_field_name]
        module_has_tasks = field.queryset.exists()
        return module_has_tasks
