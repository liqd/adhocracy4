from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseNotFound
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from adhocracy4.categories import models as category_models
from adhocracy4.filters import views as filter_views
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins

from apps.bplan import models as bplan_models
from apps.extprojects import models as extproject_models
from apps.organisations.models import Organisation

from . import blueprints
from . import forms
from . import mixins
from .filtersets import DashboardProjectFilterSet


class DashboardProjectListView(mixins.DashboardBaseMixin,
                               rules_mixins.PermissionRequiredMixin,
                               mixins.DashboardProjectPublishMixin,
                               filter_views.FilteredListView):
    model = project_models.Project
    paginate_by = 12
    filter_set = DashboardProjectFilterSet
    template_name = 'meinberlin_dashboard/project_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )


class DashboardBlueprintListView(mixins.DashboardBaseMixin,
                                 rules_mixins.PermissionRequiredMixin,
                                 generic.TemplateView):
    template_name = 'meinberlin_dashboard/blueprint_list.html'
    blueprints = blueprints.blueprints
    permission_required = 'a4projects.add_project'
    menu_item = 'project'


class DashboardProjectCreateView(mixins.DashboardProjectCreateMixin,
                                 blueprints.BlueprintMixin):
    model = project_models.Project
    form_class = forms.ProjectCreateForm
    template_name = 'meinberlin_dashboard/project_create_form.html'


class DashboardExternalProjectCreateView(mixins.DashboardProjectCreateMixin):
    model = extproject_models.ExternalProject
    form_class = forms.ExternalProjectCreateForm
    template_name = 'meinberlin_dashboard/external_project_create_form.html'

    blueprint = dict(blueprints.blueprints)['external-project']


class DashboardBplanProjectCreateView(mixins.DashboardProjectCreateMixin):
    model = bplan_models.Bplan
    form_class = forms.BplanProjectCreateForm
    template_name = 'meinberlin_dashboard/bplan_project_create_form.html'

    blueprint = dict(blueprints.blueprints)['bplan']


class DashboardProjectCreateViewDispatcher(generic.View):
    mappings = {
        'external-project': DashboardExternalProjectCreateView,
        'bplan': DashboardBplanProjectCreateView
    }

    def dispatch(self, request, *args, **kwargs):
        blueprint_slug = kwargs.get('blueprint_slug', None)
        if blueprint_slug in self.mappings:
            view = self.mappings[blueprint_slug].as_view()
        else:
            view = DashboardProjectCreateView.as_view()

        return view(request, *args, **kwargs)


class DashboardProjectUpdateViewDispatcher(mixins.DashboardBaseMixin,
                                           SingleObjectMixin,
                                           generic.View):
    model = project_models.Project

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()

        if self.get_bplan_or_none(project):
            # Attention: every bplan project is also an external project
            view = DashboardBplanProjectUpdateView.as_view()
        elif self.get_external_or_none(project):
            view = DashboardExternalProjectUpdateView.as_view()
        else:
            view = DashboardProjectUpdateView.as_view()
        return view(request, *args, **kwargs)

    @staticmethod
    def get_external_or_none(project):
        try:
            return project.externalproject
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_bplan_or_none(project):
        try:
            return project.externalproject.bplan
        except (ObjectDoesNotExist, AttributeError):
            return None


class DashboardProjectUpdateView(mixins.DashboardProjectUpdateMixin):
    model = project_models.Project
    form_class = forms.ProjectUpdateForm
    template_name = 'meinberlin_dashboard/project_update_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        qs = phase_models.Phase.objects.filter(module__project=self.object)
        kwargs['phases__queryset'] = qs

        if qs.first().module.settings_instance:
            settings_instance = qs.first().module.settings_instance
            kwargs['module_settings__instance'] = settings_instance

        kwargs['categories__queryset'] = \
            category_models.Category.objects.filter(
                module__project=self.object)

        return kwargs


class DashboardExternalProjectUpdateView(mixins.DashboardProjectUpdateMixin):
    model = extproject_models.ExternalProject
    form_class = forms.ExternalProjectUpdateForm
    template_name = 'meinberlin_dashboard/external_project_update_form.html'


class DashboardBplanProjectUpdateView(mixins.DashboardProjectUpdateMixin):
    model = bplan_models.Bplan
    form_class = forms.BplanProjectUpdateForm
    template_name = 'meinberlin_dashboard/bplan_project_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardBplanProjectUpdateView, self)\
            .get_context_data(**kwargs)
        context['display_embed_code'] = True
        return context


class DashboardOrganisationUpdateView(mixins.DashboardBaseMixin,
                                      rules_mixins.PermissionRequiredMixin,
                                      SuccessMessageMixin,
                                      generic.UpdateView):

    model = Organisation
    form_class = forms.OrganisationForm
    slug_url_kwarg = 'organisation_slug'
    template_name = 'meinberlin_dashboard/organisation_form.html'
    success_message = _('Organisation successfully updated.')
    permission_required = 'meinberlin_organisations.change_organisation'
    menu_item = 'organisation'


class DashboardProjectModeratorsView(mixins.DashboardBaseMixin,
                                     mixins.DashboardModRemovalMixin,
                                     rules_mixins.PermissionRequiredMixin,
                                     generic.UpdateView):

    model = project_models.Project
    form_class = forms.AddModeratorForm
    template_name = 'meinberlin_dashboard/project_moderators.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class DashboardProjectManagementView(mixins.DashboardBaseMixin,
                                     rules_mixins.PermissionRequiredMixin,
                                     SingleObjectMixin,
                                     generic.View):
    model = project_models.Project
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()

        management_view = get_management_view(project)
        if management_view:
            view = management_view.as_view()
            return view(request, project=project, *args, **kwargs)

        return HttpResponseNotFound()

    def get_success_url(self):
        return reverse(
            'dashboard-project-list',
            kwargs={'organisation_slug': self.organisation.slug, })


def get_management_view(project):
    """
    Test if any phase has a management_view set.

    Note, that the first management_view found is used.
    """
    for phase in project.phases:
        content = phase.content()
        if hasattr(content, 'management_view'):
            return getattr(content, 'management_view')

        return None
