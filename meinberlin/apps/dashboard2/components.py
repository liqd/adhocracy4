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
