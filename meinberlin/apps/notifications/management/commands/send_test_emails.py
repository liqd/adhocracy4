from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.comments.models import Comment
from adhocracy4.emails.mixins import SyncEmailMixin
from adhocracy4.projects.models import Project
from adhocracy4.reports import emails as reports_emails
from adhocracy4.reports.models import Report
from meinberlin.apps.bplan import emails as bplan_emails
from meinberlin.apps.bplan.models import Bplan
from meinberlin.apps.bplan.models import Statement
from meinberlin.apps.cms.models import EmailFormPage
from meinberlin.apps.contrib.emails import Email
from meinberlin.apps.ideas.models import Idea
from meinberlin.apps.notifications import emails as notification_emails
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.projects import models as project_models

User = get_user_model()


class TestEmail(SyncEmailMixin, Email):
    def get_receivers(self):
        return self.kwargs['receiver']

    def dispatch(self, object, *args, **kwargs):
        self.template_name = kwargs.pop('template_name')
        print('Sending template: {} with object "{}"'.format(
            self.template_name,
            str(object)))
        super().dispatch(object, *args, **kwargs)

    def get_context(self):
        context = super().get_context()
        context['project'] = getattr(self.object, 'project', None)
        context['contact_email'] = settings.CONTACT_EMAIL
        return context


class Command(BaseCommand):
    help = 'Send test emails to a registered user.'

    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, *args, **options):
        self.user = User.objects.get(email=options['email'])

        self._send_notifications_create_idea()
        self._send_notifications_comment_idea()
        self._send_notification_phase()
        self._send_notification_project_created()
        self._send_bplan_statement()
        self._send_bplan_update()

        self._send_report_mails()

        self._send_allauth_email_confirmation()
        self._send_allauth_password_reset()

        self._send_invitation_private_project()
        self._send_invitation_moderator()
        self._send_initiator_request()

        self._send_form_mail()

    def _send_notifications_create_idea(self):
        # Send notification for a newly created item
        action = Action.objects.filter(
            verb=Verbs.ADD.value,
            obj_content_type=ContentType.objects.get_for_model(Idea)
        ).exclude(project=None).first()
        if not action:
            raise CommandError('At least one idea is required')

        self._send_notify_create_item(action)

    def _send_notifications_comment_idea(self):
        # Send notifications for a comment on a item
        action = Action.objects.filter(
            verb=Verbs.ADD.value,
            obj_content_type=ContentType.objects.get_for_model(Comment),
            target_content_type=ContentType.objects.get_for_model(Idea)
        ).exclude(project=None).first()
        if not action:
            raise CommandError('At least one idea with a comment is required')

        self._send_notify_create_item(action)

    def _send_notify_create_item(self, action):
        TestEmail.send(
            action,
            receiver=[self.user],
            template_name=notification_emails.
            NotifyCreatorEmail.template_name)

        TestEmail.send(
            action,
            receiver=[self.user],
            template_name=notification_emails.
            NotifyFollowersOnNewItemCreated.template_name)

        TestEmail.send(
            action,
            receiver=[self.user],
            template_name=notification_emails.
            NotifyModeratorsEmail.template_name)

    def _send_notification_phase(self):
        action = Action.objects.filter(
            verb=Verbs.SCHEDULE.value
        ).first()
        TestEmail.send(
            action,
            receiver=[self.user],
            template_name=notification_emails.
            NotifyFollowersOnPhaseIsOverSoonEmail.template_name
        )

    def _send_notification_project_created(self):
        project = Project.objects.first()
        TestEmail.send(
            project,
            project=project,
            creator=self.user,
            receiver=[self.user],
            template_name=notification_emails.
            NotifyInitiatorsOnProjectCreatedEmail.template_name
        )

    def _send_bplan_statement(self):
        statement = Statement.objects.first()
        if not statement:
            raise CommandError('At least one bplan statement is required')

        TestEmail.send(
            statement,
            receiver=[self.user],
            template_name=bplan_emails.OfficeWorkerNotification.template_name
        )

        TestEmail.send(
            statement,
            receiver=[self.user],
            template_name=bplan_emails.SubmitterConfirmation.template_name
        )

    def _send_bplan_update(self):
        # Send notification for bplan update
        bplan = Bplan.objects.first()
        if not bplan:
            raise CommandError('At least one bplan field update is required')

        TestEmail.send(
            bplan,
            receiver=[self.user],
            template_name=bplan_emails.
            OfficeWorkerUpdateConfirmation.template_name
        )

    def _send_report_mails(self):
        report = Report.objects.first()
        if not report:
            raise CommandError('At least on report is required')

        TestEmail.send(
            report,
            receiver=[self.user],
            template_name=reports_emails.ReportCreatorEmail.template_name
        )

        TestEmail.send(
            report,
            receiver=[self.user],
            template_name=reports_emails.ReportModeratorEmail.template_name
        )

    def _send_allauth_password_reset(self):
        context = {"current_site": 'http://example.com/...',
                   "user": self.user,
                   "password_reset_url": 'http://example.com/...',
                   "request": None,
                   "username": self.user.username}

        TestEmail.send(self.user,
                       receiver=[self.user],
                       template_name='account/email/password_reset_key',
                       **context
                       )

    def _send_allauth_email_confirmation(self):
        context = {
            "user": self.user,
            "activate_url": 'http://example.com/...',
            "current_site": 'http://example.com/...',
            "key": 'the1454key',
        }

        TestEmail.send(
            self.user,
            receiver=[self.user],
            template_name='account/email/email_confirmation_signup',
            **context
        )

        TestEmail.send(
            self.user,
            receiver=[self.user],
            template_name='account/email/email_confirmation',
            **context
        )

    def _send_invitation_private_project(self):
        invite = project_models.ParticipantInvite.objects.first()
        if not invite:
            raise CommandError('At least one participant request is required')
        TestEmail.send(
            invite,
            receiver=[self.user],
            template_name='meinberlin_projects/emails/invite_participant'
        )

    def _send_invitation_moderator(self):
        invite = project_models.ModeratorInvite.objects.first()
        if not invite:
            raise CommandError('At least one moderator request is required')
        TestEmail.send(
            invite,
            receiver=[self.user],
            template_name='meinberlin_projects/emails/invite_moderator'
        )

    def _send_initiator_request(self):
        organisation = Organisation.objects.first()
        TestEmail.send(
            self.user,
            organisation=organisation,
            phone='01234567',
            receiver=[self.user],
            template_name='meinberlin_initiators/emails/initiator_request'
        )

    def _send_form_mail(self):
        emailformpage = EmailFormPage.objects.first()
        if not emailformpage:
            raise CommandError('At least one emailformpage obj is required')
        fields = {
            'Multi': 'some text with \n'
                     'newlines and \n'
                     'such things',
            'Single': 'just a single line of text that was entered',
            'More fields': 'more text',
            'No more fields': 'more text',
        }

        TestEmail.send(
            emailformpage,
            field_values=fields,
            receiver=[self.user],
            template_name='meinberlin_cms/emails/form_submission'
        )
