from adhocracy4.forms import widgets
from adhocracy4.labels import models as labels_models


class LabelsAddableFieldMixin:
    labels_field_name = 'labels'

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'module'):
            self.module = kwargs.pop('module')
        super().__init__(*args, **kwargs)

        field = self.fields[self.labels_field_name]
        field.queryset = labels_models.Label.objects.filter(module=self.module)
        field.required = False
        field.widget = widgets.CustomCheckboxSelectMultiple(
            choices=[(label.id, label.name) for label in field.queryset])

    def show_labels(self):
        field = self.fields[self.labels_field_name]
        module_has_labels = field.queryset.exists()
        return module_has_labels
