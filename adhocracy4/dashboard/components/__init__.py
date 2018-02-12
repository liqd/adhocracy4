__all__ = ['DashboardComponent', 'components']


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

    label : str
        The localized label to be shown in the dashboard menu if the component
        is effective

    """

    identifier = ''
    weight = 0
    label = ''

    def is_effective(self, project_or_module):
        """Return if the component is effective for the current context.

        If a component isn't effective it won't be shown in the menu or
        considered when determining the projects' progress.

        Parameters
        ----------
        project_or_module : Project or Module
            The project or module in whose context the component may
            be effective.

        Returns
        -------
        bool
            Return True if the component is effective for the passed project
            or module context.

        """
        return False

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


def _component_sort_key(component):
    return component.weight, component.identifier


class DashboardComponents:
    def __init__(self):
        self._registry = {
            'projects': {},
            'projects_replacements': {},
            'modules': {},
            'modules_replacements': {}
        }
        self._queue_replacements = True

    @property
    def projects(self):
        return self._registry['projects']

    @property
    def modules(self):
        return self._registry['modules']

    def register_project(self, component):
        self._register('projects', component)

    def register_module(self, component):
        self._register('modules', component)

    def _register(self, section, component):
        if component.identifier in self._registry[section]:
            raise ValueError('Identifier ({}) is already registered'
                             .format(component.identifier))
        self._registry[section][component.identifier] = component

    def replace_project(self, component):
        self._replace('projects', component)

    def replace_module(self, component):
        self._replace('modules', component)

    def _replace(self, section, component):
        if self._queue_replacements:
            replacement_key = '{}_replacements'.format(section)
            self._registry[replacement_key][component.identifier] = component
        else:
            self._registry[section][component.identifier] = component

    def apply_replacements(self):
        if self._queue_replacements:
            self._queue_replacements = False
            for identifier, component \
                    in self._registry['projects_replacements'].items():
                self._registry['projects'][identifier] = component
            del self._registry['projects_replacements']

            for identifier, component \
                    in self._registry['modules_replacements'].items():
                self._registry['modules'][identifier] = component
            del self._registry['modules_replacements']

    def get_project_components(self):
        return sorted(self._registry['projects'].values(),
                      key=_component_sort_key)

    def get_module_components(self):
        return sorted(self._registry['modules'].values(),
                      key=_component_sort_key)

    def get_urls(self):
        # FIXME: where to move this method
        from django.conf.urls import url

        urlpatterns = []
        for component in self.get_project_components():
            urls = component.get_urls()
            if urls:
                for pattern, view, name in urls:
                    urlpattern = url(pattern, view, name=name)
                    urlpatterns.append(urlpattern)

        for component in self.get_module_components():
            urls = component.get_urls()
            if urls:
                for pattern, view, name in urls:
                    urlpattern = url(pattern, view, name=name)
                    urlpatterns.append(urlpattern)

        return urlpatterns


components = DashboardComponents()
