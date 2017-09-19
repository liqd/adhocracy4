from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from django.views import generic

from adhocracy4.projects.models import Project
from meinberlin.apps.bplan import models as bplan_models
from meinberlin.apps.dashboard2 import mixins as a4dashboard_mixins
from meinberlin.apps.dashboard2.components.forms.views import \
    ProjectComponentFormView
from meinberlin.apps.dashboard2.views import ProjectCreateView
from meinberlin.apps.extprojects import models as extproject_models
from meinberlin.apps.newsletters.forms import NewsletterForm
from meinberlin.apps.newsletters.views import NewsletterCreateView
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.projects.models import ModeratorInvite
from meinberlin.apps.projects.models import ParticipantInvite

from . import forms

User = get_user_model()


class DashboardOrganisationUpdateView(a4dashboard_mixins.DashboardBaseMixin,
                                      SuccessMessageMixin,
                                      generic.UpdateView):

    model = Organisation
    form_class = forms.OrganisationForm
    slug_url_kwarg = 'organisation_slug'
    template_name = 'meinberlin_dashboard/organisation_form.html'
    success_message = _('Organisation successfully updated.')
    permission_required = 'meinberlin_organisations.change_organisation'
    menu_item = 'organisation'


class DashboardNewsletterCreateView(a4dashboard_mixins.DashboardBaseMixin,
                                    NewsletterCreateView):
    template_name = 'meinberlin_dashboard/newsletter_form.html'
    menu_item = 'newsletter'
    form_class = NewsletterForm
    permission_required = 'a4projects.add_project'

    def get_email_kwargs(self):
        kwargs = {}
        kwargs.update({'organisation_pk': self.organisation.pk})
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation'] = self.organisation
        kwargs.pop('user')
        return kwargs

    def get_success_url(self):
        return reverse(
            'a4dashboard:newsletter-create',
            kwargs={'organisation_slug': self.organisation.slug})


class ExternalProjectCreateView(ProjectCreateView):

    model = extproject_models.ExternalProject
    slug_url_kwarg = 'project_slug'
    blueprint_key = 'external-project'
    form_class = forms.ExternalProjectCreateForm
    template_name = 'meinberlin_dashboard/external_project_create_form.html'


class ExternalProjectUpdateView(ProjectComponentFormView):

    model = extproject_models.ExternalProject

    def get_project(self, *args, **kwargs):
        project = super().get_project(*args, **kwargs)
        return project.externalproject

    def get_object(self, queryset=None):
        return self.project

    def validate_object_project(self):
        return True

    def validate_object_module(self):
        return True


class BplanProjectCreateView(ExternalProjectCreateView):

    model = bplan_models.Bplan
    slug_url_kwarg = 'project_slug'
    blueprint_key = 'bplan'
    form_class = forms.BplanProjectCreateForm
    template_name = 'meinberlin_dashboard/external_project_create_form.html'


class BplanProjectUpdateView(ProjectComponentFormView):

    model = bplan_models.Bplan

    def get_project(self, *args, **kwargs):
        project = super().get_project(*args, **kwargs)
        return project.externalproject.bplan

    def get_object(self, queryset=None):
        return self.project

    def validate_object_project(self):
        return True

    def validate_object_module(self):
        return True


class AbstractProjectUserListView(a4dashboard_mixins.DashboardComponentMixin,
                                  a4dashboard_mixins.DashboardBaseMixin,
                                  a4dashboard_mixins.DashboardContextMixin,
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
        if 'submit_action' in request.POST:
            if request.POST['submit_action'] == 'remove_user':
                pk = int(request.POST['user_pk'])
                user = get_object_or_404(User, pk=pk)

                if request.POST['submit_action'] == 'remove_user':
                    related_users = getattr(self.object,
                                            self.related_users_field)
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


class AbstractProjectUserInviteListView(AbstractProjectUserListView):
    form_class = forms.InviteUsersFromEmailForm
    invite_model = None

    def post(self, request, *args, **kwargs):

        if 'submit_action' in request.POST and (
                request.POST['submit_action'] == 'remove_invite'):
            pk = int(request.POST['invite_pk'])
            invite = self.invite_model.objects.get(pk=pk)
            invite.delete()
            messages.success(request, _('Invitation succesfully removed.'))
        return super().post(request, *args, **kwargs)

    def filter_existing(self, emails):
        related_users = getattr(self.object, self.related_users_field)
        related_emails = [u.email for u in related_users.all()]
        existing = []
        filtered_emails = []
        for email in emails:
            if email in related_emails:
                existing.append(email)
            else:
                filtered_emails.append(email)
        return filtered_emails, existing

    def filter_pending(self, emails):
        pending = []
        filtered_emails = []
        for email in emails:
            if self.invite_model.objects.filter(email=email).exists():
                pending.append(email)
            else:
                filtered_emails.append(email)
        return filtered_emails, pending

    def form_valid(self, form):
        emails = form.cleaned_data['add_users']

        emails, existing = self.filter_existing(emails)
        if existing:
            messages.error(
                self.request,
                _('Following users already accepted an invitation: ') +
                ', '.join(existing)
            )

        emails, pending = self.filter_pending(emails)
        if pending:
            messages.error(
                self.request,
                _('Following users are already invited: ') +
                ', '.join(pending)
            )

        for email in emails:
            self.invite_model.objects.invite(
                self.request.user,
                self.project,
                email
            )

        messages.success(
            self.request,
            ungettext(self.success_message[0], self.success_message[1],
                      len(emails)).format(len(emails))
        )

        return redirect(self.get_success_url())


class DashboardProjectModeratorsView(AbstractProjectUserInviteListView):

    model = Project
    slug_url_kwarg = 'project_slug'
    template_name = 'meinberlin_dashboard/project_moderators.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    related_users_field = 'moderators'
    add_user_field_label = _('Invite moderators via email')
    success_message = ('{} moderator invited.', '{} moderators invited.')
    success_message_removal = _('Moderator successfully removed.')

    invite_model = ModeratorInvite


class DashboardProjectParticipantsView(AbstractProjectUserInviteListView):

    model = Project
    slug_url_kwarg = 'project_slug'
    template_name = 'meinberlin_dashboard/project_participants.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    related_users_field = 'participants'
    add_user_field_label = _('Invite users via email')
    success_message = ('{} participant invited.', '{} participants invited.')
    success_message_removal = _('Participant successfully removed.')

    invite_model = ParticipantInvite
