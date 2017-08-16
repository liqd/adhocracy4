class DashboardComponent:
    """Abstract interface for dashboard components.

    Required properties:
    - app_label

    Required properties with default implementation:
    - label (defaults to the lower class name)
    - identifier (defaults to "app_label:label")
      - has to be unique
      - may only contain alphanumeric characters and -, _, :
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


class DashboardProjectComponent(DashboardComponent):
    """Abstract interface for project components.

    Inherits from DashboardComponent.

    Required methods: str | None
    - get_menu_item(project):
      Return a localized string if the component should be rendered for the
      project passed. Return None otherwise
    """

    def get_menu_item(self, project):
        pass


class DashboardModuleComponent(DashboardComponent):
    """Abstract interface for module components.

    Inherits from DashboardComponent.

    Required methods: str | None
    - get_menu_item(module):
      Return a localized string if the component should be rendered for the
      module passed. Return None otherwise
    """

    def get_menu_item(self, module):
        pass
