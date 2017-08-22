from django.core.exceptions import FieldDoesNotExist
from django.urls import reverse


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

    """

    identifier = ''

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


class ProjectFormComponent(DashboardComponent):
    """Abstract project related dashboard component based on forms.

    This abstract component is used to make components from forms inheriting
    from ProjectDashboardForm.
    It allows to simply pass the form and some additional configuration
    properties to create a valid component.
    The components are registering urls based on the the unique identifier
    and are using ProjectComponentFormView to handle the form processing.
    Forms inheriting from ProjectDashboardForm may be configured with an
    additional Meta.required attribute which defines the form fields that have
    to be validly entered prior to project publishing. The component provides
    a get_progress implementation based on this list and prevents from removing
    required data if the project is published.

    Properties
    ----------
    menu_label : str
        This label is always returned regardless of project state
    form_title : str
        This title is shown on top of the rendered form
    form_class : ProjectDashboardForm
        This is the form class used to render from the ProjectComponentFormView

    """

    menu_label = ''
    form_title = ''
    form_class = None
    form_template_name = ''

    def get_menu_label(self, project):
        return self.menu_label

    def get_base_url(self, project_or_module):
        name = 'a4dashboard:dashboard-{identifier}-edit'.format(
            identifier=self.identifier)
        return reverse(name, args=[project_or_module.slug])

    def get_urls(self):
        from .views import ProjectComponentFormView
        view = ProjectComponentFormView.as_view(
            component=self,
            title=self.form_title,
            form_class=self.form_class,
            form_template_name=self.form_template_name
        )
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/{identifier}/$'.format(
                identifier=self.identifier),
            view,
            'dashboard-{identifier}-edit'.format(identifier=self.identifier)
        )]

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
    """Abstract module related dashboard component based on forms.

    This abstract component is used to make components from forms inheriting
    from ModuleDashboardForm.
    It allows to simply pass the form and some additional configuration
    properties to create a valid component.
    The components are registering urls based on the the unique identifier
    and are using ModuleComponentFormView to handle the form processing.
    Forms inheriting from ModuleDashboardForm may be configured with an
    additional Meta.required attribute which defines the form fields that have
    to be validly entered prior to project publishing. The component provides
    a get_progress implementation based on this list and prevents from removing
    required data if the project is published.

    Properties
    ----------
    menu_label : str
        This label is always returned regardless of module state
    form_title : str
        This title is shown on top of the rendered form
    form_class : ModuleDashboardForm
        This is the form class used to render from the ModuleComponentFormView

    """

    def get_base_url(self, project_or_module):
        name = 'a4dashboard:dashboard-{identifier}-edit'.format(
            identifier=self.identifier)
        return reverse(name, args=[project_or_module.slug])

    def get_urls(self):
        from .views import ModuleComponentFormView
        view = ModuleComponentFormView.as_view(
            component=self,
            title=self.form_title,
            form_class=self.form_class,
            form_template_name=self.form_template_name
        )

        return [(
            r'^modules/(?P<module_slug>[-\w_]+)/{identifier}/$'.format(
                identifier=self.identifier),
            view,
            'dashboard-{identifier}-edit'.format(identifier=self.identifier)
        )]


class ModuleFormSetComponent(ModuleFormComponent):
    """Abstract module related dashboard component based on formsets.

    This abstract component is used to make components from forms inheriting
    from ModuleDashboardFormSet.
    It allows to simply pass the form and some additional configuration
    properties to create a valid component.
    The components are registering urls based on the the unique identifier
    and are using ModuleComponentFormView to handle the form processing.
    Forms inheriting from ModuleDashboardFormSet may be configured with an
    additional Meta.required attribute which defines the form fields that have
    to be validly entered prior to project publishing. The component provides
    a get_progress implementation based on this list and prevents from removing
    required data if the project is published.

    Properties
    ----------
    menu_label : str
        This label is always returned regardless of module state
    form_title : str
        This title is shown on top of the rendered form
    form_class : ModuleDashboardFormSet
        This is the form class used to render from the ModuleComponentFormView

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
