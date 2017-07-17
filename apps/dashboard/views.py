from functools import lru_cache

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
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
from apps.projects.emails import InviteParticipantEmail
from apps.users.models import User

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


class DashboardExternalProjectCreateView(mixins.DashboardProjectCreateMixin,
                                         blueprints.BlueprintMixin):
    model = extproject_models.ExternalProject
    form_class = forms.ExternalProjectCreateForm
    template_name = 'meinberlin_dashboard/external_project_create_form.html'


class DashboardBplanProjectCreateView(mixins.DashboardProjectCreateMixin,
                                      blueprints.BlueprintMixin):
    model = bplan_models.Bplan
    form_class = forms.BplanProjectCreateForm
    template_name = 'meinberlin_dashboard/bplan_project_create_form.html'


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


class AbstractProjectUserListView(mixins.DashboardBaseMixin,
                                  rules_mixins.PermissionRequiredMixin,
                                  generic.base.TemplateResponseMixin,
                                  generic.edit.FormMixin,
                                  generic.detail.SingleObjectMixin,
                                  generic.edit.ProcessFormView):

    form_class = forms.AddUsersFromEmailForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'submit_action' in request.POST and (
                request.POST['submit_action'] == 'remove_user'):
            pk = int(request.POST['user_pk'])
            user = get_object_or_404(User, pk=pk)

            if request.POST['submit_action'] == 'remove_user':
                related_users = getattr(self.object, self.related_users_field)
                related_users.remove(user)
                messages.success(request, self.success_message_removal)

            return redirect(self.get_success_url())
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if form.missing:
            messages.error(
                self.request,
                _('Following emails are not registered: ') + ', '.join(
                    form.missing)
            )

        if form.cleaned_data['add_users']:
            users = form.cleaned_data['add_users']
            related_users = getattr(self.object,
                                    self.related_users_field)
            related_users.add(*users)

            messages.success(
                self.request,
                ungettext(self.success_message[0], self.success_message[1],
                          len(users)).format(len(users))
            )

        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label'] = self.add_user_field_label
        return kwargs


class DashboardProjectParticipantsView(AbstractProjectUserListView):

    model = project_models.Project
    template_name = 'meinberlin_dashboard/project_participants.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    related_users_field = 'participants'
    add_user_field_label = _('Add users via email')
    success_message = ('{} user added.', '{} users added.')
    success_message_removal = _('User successfully removed.')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Send invitation mails to the new participants
        users = form.cleaned_data.get('add_users', None)
        if users:
            participant_ids = [user.id for user in users]
            InviteParticipantEmail.send(self.object,
                                        participant_ids=participant_ids)

        return response


class DashboardProjectModeratorsView(AbstractProjectUserListView):

    model = project_models.Project
    template_name = 'meinberlin_dashboard/project_moderators.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    related_users_field = 'moderators'
    add_user_field_label = _('Add moderators via email')
    success_message = ('{} moderator added.', '{} moderators added.')
    success_message_removal = _('Moderator successfully removed.')


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


@lru_cache()
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
