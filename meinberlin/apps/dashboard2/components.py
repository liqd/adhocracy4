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
        meta = getattr(self.form_class, 'Meta', None)
        required_fields = getattr(meta, 'required', None)

        if not required_fields:
            return 0, 0

        if required_fields == '__all__':
            required_fields = list(self.form_class.base_fields)

        num_valid = num_required = len(required_fields)
        for field_name in required_fields:
            try:
                field = object._meta.get_field(field_name)
                value = getattr(object, field_name, None)

                if value is None or value in field.empty_values:
                    num_valid = num_valid - 1
            except FieldDoesNotExist:
                pass

        return num_valid, num_required


class ModuleFormComponent(ProjectFormComponent):

    def get_view(self):
        from .views import ModuleComponentFormView
        return ModuleComponentFormView.as_view(
            title=self.form_title,
            form_class=self.form_class,
            form_template_name=self.form_template_name
        )
