from django.core.exceptions import FieldDoesNotExist


class DashboardComponent:
    """Abstract interface for dashboard components.

    Required properties:
    - app_label

    Required properties with default implementation:
    - label (defaults to the lower class name)
    - identifier (defaults to "app_label-label")
      - has to be unique
      - may only contain alphanumeric characters, _ and -
      - Note: is is recommended to define a custom unique identifier as
        otherwise the app_label is exposed in dashboard urls.

    Required methods:
    - get_menu_label(project_or_module): str | None
      In case of a component registered for modules the module to edit is
      passed. In case of a component registered for projects the project.
      Return a localized string if the component should be rendered for the
      project or module passed. Return None otherwise.

    - get_progress(): (int, int)
      Return a tuple containing the number of valid "input fields" as first
      element and the total number of "input fields" as the second.

    - get_urls(): [(urlpattern, view, name), ...]
      Return a list of urls to register for this component.
      Each list item has to be a triple of the urlpattern, a view function and
      an url name.
      May return None if no additional urls are required. In that case a custom
      get_view method has to be provided.

    Required methods with default implementation:
    - get_view(): view function
      Return a view function which takes menu and project/module as kwargs.
      This view is linked from the dashboard menu.
      By default the view of the first url from get_urls is returned.
    """

    app_label = None

    @property
    def label(self):
        return self.__class__.__name__.lower()

    @property
    def identifier(self):
        return '{app_label}-{component_label}'.format(
            app_label=self.app_label,
            component_label=self.label,
        )

    def get_menu_label(self, project_or_module):
        pass

    def get_progress(self, project_or_module):
        return 0, 0

    def get_urls(self):
        pass

    def get_view(self):
        _, view, _ = self.get_urls()[0]
        return view


class ProjectFormComponent(DashboardComponent):
    """Abstract interface for project dashboard components based on forms.

    This component is intended to be used with ProjectDashboardForm.
    It will always return a ProjectComponentFormView
    and provides a default implementation for get_progress.

    Required properties:
    - menu_label: str
      This label is always returned regardless of project state
    - form_title: str
      This title is shown on top of the rendered form
    - form_class: ProjectDashboardForm
      This is the form class used to render from the ProjectComponentFormView
    """

    menu_label = ''
    form_title = ''
    form_class = None
    form_template_name = ''

    def get_menu_label(self, project):
        return self.menu_label

    def get_view(self):
        from .views import ProjectComponentFormView
        return ProjectComponentFormView.as_view(
            component=self,
            title=self.form_title,
            form_class=self.form_class,
            form_template_name=self.form_template_name
        )

    def get_progress(self, object):
        required_fields = self.form_class.get_required_fields()
        if required_fields == '__all__':
            required_fields = self._get_all_required_fields(self.form_class,
                                                            object)

        if not required_fields:
            return 0, 0

        return self._get_progress_for_object(object, required_fields)

    @staticmethod
    def _get_all_required_fields(form_class, model):
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
    """Abstract interface for module dashboard components based on forms.

    This component is intended to be used with ModuleDashboardForm.
    It will always return a ModuleComponentFormView
    and provides a default implementation for get_progress.

    Required properties:
    - menu_label: str
      This label is always returned regardless of project state
    - form_title: str
      This title is shown on top of the rendered form
    - form_class: ModuleDashboardForm
      This is the form class used to render from the ModuleComponentFormView
    """

    def get_view(self):
        from .views import ModuleComponentFormView
        return ModuleComponentFormView.as_view(
            component=self,
            title=self.form_title,
            form_class=self.form_class,
            form_template_name=self.form_template_name
        )


class ModuleFormSetComponent(ModuleFormComponent):
    """Abstract interface for module dashboard components based on formsets.

    This component is intended to be used with ModuleDashboardFormSet.
    It will always return a ModuleComponentFormView
    and provides a default implementation for get_progress.

    Required properties:
    - menu_label: str
      This label is always returned regardless of project state
    - form_title: str
      This title is shown on top of the rendered form
    - form_class: ModuleDashboardFormSet
      This is the formset class used to render from the ModuleComponentFormView
    """

    def get_progress(self, parent):
        child_form_class = self.form_class.form
        child_model = child_form_class._meta.model

        required_fields = self.form_class.get_required_fields()
        if required_fields == '__all__':
            required_fields = self._get_all_required_fields(child_form_class,
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
