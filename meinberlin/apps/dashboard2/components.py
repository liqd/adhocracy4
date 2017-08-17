from django.core.exceptions import FieldDoesNotExist


class DashboardComponent:
    """Abstract interface for dashboard components.

    Required properties:
    - app_label

    Required properties with default implementation:
    - label (defaults to the lower class name)
    - identifier (defaults to "app_label:label")
      - has to be unique
      - may only contain alphanumeric characters and -, _, :
      - Note: is is recommended to define a custom unique identifier as
        otherwise the app_label is exposed in dashboard urls.

    Required methods:
    - get_menu_label(project_or_module): str | None
      In case of a component registered for modules the module to edit is
      passed. In case of a component registered for projects the project.
      Return a localized string if the component should be rendered for the
      project or module passed. Return None otherwise.

    - get_view(): view function
      Return a view function which takes menu and project/module as kwargs
    """

    app_label = None

    @property
    def label(self):
        return self.__class__.__name__.lower()

    @property
    def identifier(self):
        return '{app_label}:{component_label}'.format(
            app_label=self.app_label,
            component_label=self.label,
        )

    def get_menu_label(self, project_or_module):
        pass

    def get_view(self):
        pass

    def get_progress(self, project_or_module):
        return 0, 0


class ProjectFormComponent(DashboardComponent):

    menu_label = ''
    form_title = ''
    form_class = ''
    form_template_name = ''

    def get_menu_label(self, project):
        return self.menu_label

    def get_view(self):
        from .views import ProjectComponentFormView
        return ProjectComponentFormView.as_view(
            title=self.form_title,
            form_class=self.form_class,
            form_template_name=self.form_template_name
        )

    def get_progress(self, object):
        required_fields = self._get_required_fields(self.form_class, object)

        if not required_fields:
            return 0, 0

        return self._get_progress_for_object(object, required_fields)

    @staticmethod
    def _get_required_fields(form_class, model):
        meta = getattr(form_class, 'Meta', None)
        required_fields = getattr(meta, 'required', [])

        if required_fields == '__all__':
            required_fields = []
            for field_name in form_class.base_fields.keys():
                try:
                    field = model._meta.get_field(field_name)
                    if field.concrete:
                        required_fields.append(field_name)
                except FieldDoesNotExist:
                    pass

        return required_fields

    @staticmethod
    def _get_progress_for_object(object, required_fields):
        num_valid = num_required = len(required_fields)
        for field_name in required_fields:
            field = object._meta.get_field(field_name)
            value = getattr(object, field_name, None)

            if value is None or value in field.empty_values:
                num_valid = num_valid - 1

        return num_valid, num_required


class ModuleFormComponent(ProjectFormComponent):

    def get_view(self):
        from .views import ModuleComponentFormView
        return ModuleComponentFormView.as_view(
            title=self.form_title,
            form_class=self.form_class,
            form_template_name=self.form_template_name
        )


class ModuleFormSetComponent(ModuleFormComponent):

    def get_progress(self, parent):
        child_form_class = self.form_class.form
        child_model = child_form_class._meta.model

        required_fields = self._get_required_fields(child_form_class,
                                                    child_model)

        if not required_fields:
            return 0, 0

        # Attention: this could break if additional args
        # would be expected by the formset.
        formset = self.form_class(instance=parent)

        num_valid = 0
        num_required = 0
        for child in formset.queryset:
            num_valid_obj, num_required_obj = \
                self._get_progress_for_object(child, required_fields)
            num_valid = num_valid + num_valid_obj
            num_required = num_required + num_required_obj

        return num_valid, num_required
