from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.projects.emails import InviteParticipantEmail

from . import blueprints
from . import content
from . import forms
from . import mixins

User = get_user_model()


def get_object_or_none(*args, **kwargs):
    try:
        return get_object_or_404(*args, **kwargs)
    except Http404:
        return None


class ProjectListView(mixins.DashboardBaseMixin,
                      generic.ListView):
    model = project_models.Project
    paginate_by = 12
    template_name = 'meinberlin_dashboard2/project_list.html'
    permission_required = 'a4projects.add_project'

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )


class BlueprintListView(mixins.DashboardBaseMixin,
                        generic.TemplateView):
    blueprints = blueprints.blueprints
    template_name = 'meinberlin_dashboard2/blueprint_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'


class ProjectCreateView(mixins.DashboardBaseMixin,
                        mixins.BlueprintMixin,
                        generic.CreateView,
                        SuccessMessageMixin):
    model = project_models.Project
    form_class = forms.ProjectCreateForm
    template_name = 'meinberlin_dashboard2/project_create_form.html'
    permission_required = 'a4projects.add_project'
    success_message = _('Project succesfully created.')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['type'] = self.blueprint_key
        kwargs['organisation'] = self.organisation
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('a4dashboard:project-edit',
                       kwargs={'project_slug': self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)

        # FIXME: maybe replace by dashboard signals
        self._create_modules_and_phases(self.object)

        return response

    def _create_modules_and_phases(self, project):
        module = module_models.Module(
            name='Onlinebeteiligung',
            description=project.description,
            weight=1,
            project=project,
        )
        module.save()
        self._create_module_settings(module)
        self._create_phases(module, self.blueprint.content)

    def _create_module_settings(self, module):
        settings_model = apps.get_model(*self.blueprint.settings_model)
        module_settings = settings_model(module=module)
        module_settings.save()

    def _create_phases(self, module, blueprint_phases):
        for phase_content in blueprint_phases:
            phase = phase_models.Phase(
                type=phase_content.identifier,
                name=phase_content.name,
                description=phase_content.description,
                weight=phase_content.weight,
                module=module,
            )
            phase.save()


class ProjectUpdateView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        project = get_object_or_404(project_models.Project,
                                    slug=kwargs['project_slug'])
        components = content.get_project_components()
        component = components[0]
        return component.get_base_url(project)


class ProjectPublishView(mixins.DashboardBaseMixin,
                         SingleObjectMixin,
                         generic.View):
    permission_required = 'a4projects.add_project'
    model = project_models.Project
    slug_url_kwarg = 'project_slug'

    def post(self, request, *args, **kwargs):
        self.project = self.get_object()

        action = request.POST.get('action', None)
        if action == 'publish':
            self.publish_project()
        elif action == 'unpublish':
            self.unpublish_project()
        else:
            messages.warning(self.request, _('Invalid action'))

        return HttpResponseRedirect(self.get_next())

    def get_next(self):
        if 'referrer' in self.request.POST:
            return self.request.POST['referrer']
        elif 'HTTP_REFERER' in self.request.META:
            return self.request.META['HTTP_REFERER']

        return reverse('project-edit', kwargs={
            'project_slug': self.project.slug
        })

    def publish_project(self):
        if not self.project.is_draft:
            messages.info(self.request, _('Project is already published'))
            return

        # FIXME: Move logic somewhere else
        progress = mixins.DashboardContextMixin\
            .get_project_progress(self.project)
        is_complete = progress['valid'] == progress['required']

        if not is_complete:
            messages.error(self.request,
                           _('Project cannot be published. '
                             'Required fields are missing.'))
            return

        self.project.is_draft = False
        self.project.save()
        messages.success(self.request,
                         _('Project successfully published.'))

    def unpublish_project(self):
        if self.project.is_draft:
            messages.info(self.request, _('Project is already unpublished'))
            return

        self.project.is_draft = True
        self.project.save()
        messages.success(self.request,
                         _('Project successfully unpublished.'))


class ProjectComponentFormView(mixins.DashboardBaseMixin,
                               mixins.DashboardComponentMixin,
                               mixins.DashboardContextMixin,
                               SuccessMessageMixin,
                               generic.UpdateView):

    permission_required = 'a4projects.add_project'
    model = project_models.Project
    template_name = 'meinberlin_dashboard2/base_form_project.html'
    success_message = _('Project successfully updated.')

    # Properties to be set when calling as_view()
    component = None
    title = ''
    form_class = None
    form_template_name = ''

    def get_object(self, queryset=None):
        return self.project


class ModuleComponentFormView(mixins.DashboardComponentMixin,
                              mixins.DashboardBaseMixin,
                              mixins.DashboardContextMixin,
                              SuccessMessageMixin,
                              generic.UpdateView):

    permission_required = 'a4projects.add_project'
    model = module_models.Module
    template_name = 'meinberlin_dashboard2/base_form_module.html'
    success_message = _('Module successfully updated.')

    # Properties to be set when calling as_view()
    component = None
    title = ''
    form_class = None
    form_template_name = ''

    def get_object(self, queryset=None):
        return self.module


class AbstractProjectUserListView(mixins.DashboardComponentMixin,
                                  mixins.DashboardBaseMixin,
                                  mixins.DashboardContextMixin,
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


class DashboardProjectModeratorsView(AbstractProjectUserListView):

    model = project_models.Project
    slug_url_kwarg = 'project_slug'
    template_name = 'meinberlin_dashboard2/project_moderators.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    related_users_field = 'moderators'
    add_user_field_label = _('Add moderators via email')
    success_message = ('{} moderator added.', '{} moderators added.')
    success_message_removal = _('Moderator successfully removed.')


class DashboardProjectParticipantsView(AbstractProjectUserListView):

    model = project_models.Project
    slug_url_kwarg = 'project_slug'
    template_name = 'meinberlin_dashboard2/project_participants.html'
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
