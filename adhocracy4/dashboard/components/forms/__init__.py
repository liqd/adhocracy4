from django.core.exceptions import FieldDoesNotExist
from django.urls import reverse

from .. import DashboardComponent
from .forms import ModuleDashboardForm
from .forms import ModuleDashboardFormSet
from .forms import ProjectDashboardForm

__all__ = ['ProjectFormComponent', 'ProjectDashboardForm',
           'ModuleFormComponent', 'ModuleDashboardForm',
           'ModuleFormSetComponent', 'ModuleDashboardFormSet']


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
    Form components are always effective.

    Properties
    ----------
    form_title : str
        This title is shown on top of the rendered form
    form_class : ProjectDashboardForm
        This is the form class used to render from the ProjectComponentFormView

    """

    form_title = ''
    form_class = None
    form_template_name = ''

    def is_effective(self, project):
        return True

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

            if not field.many_to_many:
                if value is None or value in field.empty_values:
                    num_valid = num_valid - 1
            else:
                if not value.exists():
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
    Form components are always effective.

    Properties
    ----------
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
    Form components are always effective.

    Properties
    ----------
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
