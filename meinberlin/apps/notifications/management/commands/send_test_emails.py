from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.comments.models import Comment
from adhocracy4.projects.models import Project
from adhocracy4.reports import emails as reports_emails
from adhocracy4.reports.models import Report
from apps.bplan import emails as bplan_emails
from apps.bplan.models import Statement
from apps.contrib.emails import Email
from apps.ideas.models import Idea
from apps.notifications import emails as notification_emails

User = get_user_model()


class TestEmail(Email):
    def get_receivers(self):
        return self.kwargs['receiver']

    def dispatch(self, object, *args, **kwargs):
        self.template_name = kwargs.pop('template_name')
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
        self._send_bplan_statement()

        self._send_report_mails()

        self._send_allauth_email_confirmation()
        self._send_allauth_password_reset()

        self._send_invitation_private_project()

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
        project = Project.objects.first()
        TestEmail.send(
            project,
            receiver=[self.user],
            template_name='meinberlin_projects/email/invite_participant'
        )
