class DashboardComponent:
    """Interface for dashboard components.

    Dashboard components are globally registered by their unique identifier.
    Every dashboard component is used to configure either a project
    or a module.
    They define the urlpatterns and views required for configuration
    and provide an url which acts as the base entry point.
    Dashboard components keep track of the projects publish progress.
    A project may only be published if every component progress is complete.
    If a project is published, the component has to ensure that its progress
    does not regress. (F.ex. fields required for publishing may not be updated
    with a blank value after publishing).


    Properties
    ----------
    identifier : str
        Unique identifier of the component.
        May only contain alphanumeric characters, _, and -
        F.ex. an unique identifier would be '{app_label}-{component_name}'.
        The identifier is used to register and retrieve components from the
        registry. It may be used to define unique url names.

    weight : int
        Weight of the component.
        Used to sort components within the dashboard menu.
        The component with the lowest weight will be the default entry point
        for editing a project.

    """

    identifier = ''
    weight = 0

    def get_menu_label(self, project_or_module):
        """Return the menu label if the component should be shown.

        Parameters
        ----------
        project_or_module : Project or Module
            The project or module in whose context the component
            should be shown.

        Returns
        -------
        str
            Return the localized label to be shown in the dashboard menu or
            '' if the component should not be shown for the passed project or
            module context.

        """
        return ''

    def get_progress(self, project_or_module):
        """Return the progress of this component.

        Parameters
        ----------
        project_or_module : Project or Module
            The project or module in whose context the component's progress
            should be determined.

        Returns
        -------
        (int, int)
            Return a tuple containing the number of valid "input fields" as
            the first element and the total number of "input fields" as the
            second element.
            If no input fields are required (0, 0) should be returned.

        """
        return 0, 0

    def get_urls(self):
        """Return the urls needed for this component.

        The urls are registered under the prefix of the dashboard and within
        its `a4dashboard` namespace.

        Returns
        -------
        list of (str, func, str)
            Return a list of triples containing
            the urlpattern as a string,
            the view function,
            and the view name.

        """
        return []

    def get_base_url(self, project_or_module):
        """Return the url that acts as the base entry point for the component.

        The url is linked from the dashboard menu.

        Parameters
        ----------
        project_or_module : Project or Module
            The project or module to whose context the component base link
            should resolve

        Returns
        -------
        str
            Return the url to the base view of this component.

        """
        return ''
