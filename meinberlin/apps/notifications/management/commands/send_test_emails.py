from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.comments.models import Comment
from adhocracy4.emails.mixins import SyncEmailMixin
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project
from adhocracy4.reports import emails as reports_emails
from adhocracy4.reports.models import Report
from meinberlin.apps.bplan import emails as bplan_emails
from meinberlin.apps.bplan.models import Bplan
from meinberlin.apps.bplan.models import Statement
from meinberlin.apps.budgeting.models import Proposal
from meinberlin.apps.cms.models import EmailFormPage
from meinberlin.apps.contrib.emails import Email
from meinberlin.apps.ideas.models import Idea
from meinberlin.apps.notifications import emails as notification_emails
from meinberlin.apps.offlineevents.models import OfflineEvent
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.projects import models as project_models

User = get_user_model()


class TestEmail(SyncEmailMixin, Email):
    def get_receivers(self):
        return self.kwargs["receiver"]

    def dispatch(self, object, *args, **kwargs):
        self.template_name = kwargs.pop("template_name")
        print(
            'Sending template: {} with object "{}"'.format(
                self.template_name, str(object)
            )
        )
        super().dispatch(object, *args, **kwargs)

    def get_context(self):
        context = super().get_context()
        context["project"] = getattr(self.object, "project", None)
        context["contact_email"] = settings.CONTACT_EMAIL
        return context


class Command(BaseCommand):
    help = "Send test emails to a registered user."

    def add_arguments(self, parser):
        parser.add_argument("email")

    def handle(self, *args, **options):
        self.user = User.objects.get(email=options["email"])

        self._send_notifications_create_idea()
        self._send_notifications_comment_idea()
        self._send_notifications_on_moderator_feedback()

        self._send_notification_phase()
        self._send_notification_offlineevent()

        self._send_notification_project_created()
        self._send_bplan_statement()
        self._send_bplan_update()

        self._send_report_mails()

        self._send_invitation_private_project()
        self._send_invitation_moderator()
        self._send_initiator_request()

        self._send_welcome_email()

        self._send_form_mail()

        self._send_allauth_email_confirmation()
        self._send_allauth_password_reset()
        self._send_allauth_unknown_account()
        self._send_allauth_account_already_exists()

    def _send_notifications_create_idea(self):
        # Send notification for a newly created item
        action = (
            Action.objects.filter(
                verb=Verbs.ADD.value,
                obj_content_type=ContentType.objects.get_for_model(Idea),
            )
            .exclude(project=None)
            .first()
        )
        if not action:
            self.stderr.write("At least one idea is required")
            return

        self._send_notify_create_item(action)

    def _send_notifications_comment_idea(self):
        # Send notifications for a comment on a item
        action = (
            Action.objects.filter(
                verb=Verbs.ADD.value,
                obj_content_type=ContentType.objects.get_for_model(Comment),
                target_content_type=ContentType.objects.get_for_model(Idea),
            )
            .exclude(project=None)
            .first()
        )
        if not action:
            self.stderr.write("At least one idea with a comment is required")
            return

        self._send_notify_create_item(action)

    def _send_notify_create_item(self, action):
        TestEmail.send(
            action,
            receiver=[self.user],
            template_name=notification_emails.NotifyCreatorEmail.template_name,
        )

        TestEmail.send(
            action,
            receiver=[self.user],
            template_name=notification_emails.NotifyModeratorsEmail.template_name,
        )

    def _send_notifications_on_moderator_feedback(self):
        moderated_idea = Idea.objects.filter(
            moderator_feedback_text__isnull=False
        ).first()
        if not moderated_idea:
            self.stderr.write("At least one idea with moderator feedback is required")
            return

        TestEmail.send(
            moderated_idea,
            receiver=[self.user],
            send_to_creator=True,
            template_name=notification_emails.NotifyCreatorOrContactOnModeratorFeedback.template_name,
        )

        moderated_proposal = Proposal.objects.filter(
            moderator_feedback_text__isnull=False
        ).first()
        if not moderated_proposal:
            self.stderr.write(
                "At least one proposal with moderator feedback is required"
            )
            return

        TestEmail.send(
            moderated_proposal,
            receiver=[self.user],
            template_name=notification_emails.NotifyCreatorOrContactOnModeratorFeedback.template_name,
        )

    def _send_notification_phase(self):
        phase = Phase.objects.filter(start_date__isnull=False).first()
        if not phase:
            self.stderr.write("At least one phase with dates is required")
            return
        action = Action.objects.create(
            verb=Verbs.SCHEDULE,
            obj_content_type=ContentType.objects.get_for_model(Phase),
            obj=phase,
            project=phase.module.project,
        )

        TestEmail.send(
            action,
            receiver=[self.user],
            template_name=notification_emails.NotifyFollowersOnPhaseIsOverSoonEmail.template_name,
        )
        action.delete()

        action = Action.objects.create(
            verb=Verbs.START,
            obj_content_type=ContentType.objects.get_for_model(Phase),
            obj=phase,
            project=phase.module.project,
        )

        TestEmail.send(
            action,
            receiver=[self.user],
            template_name=notification_emails.NotifyFollowersOnPhaseStartedEmail.template_name,
        )
        action.delete()

    def _send_notification_offlineevent(self):
        offlineevent = OfflineEvent.objects.first()
        if not offlineevent:
            self.stderr.write("At least one offline event is required")
            return
        action = Action.objects.create(
            obj_content_type=ContentType.objects.get_for_model(OfflineEvent),
            obj=offlineevent,
            project=offlineevent.project,
            verb=Verbs.SCHEDULE,
        )

        TestEmail.send(
            action,
            receiver=[self.user],
            template_name=notification_emails.NotifyFollowersOnUpcomingEventEmail.template_name,
        )
        action.delete()

    def _send_notification_project_created(self):
        project = Project.objects.first()
        TestEmail.send(
            project,
            project=project,
            creator=self.user,
            receiver=[self.user],
            template_name=notification_emails.NotifyInitiatorsOnProjectCreatedEmail.template_name,
        )

    def _send_bplan_statement(self):
        statement = Statement.objects.first()
        identifier = statement.module.project.externalproject.bplan.identifier
        if not statement:
            self.stderr.write("At least one bplan statement is required")
            return

        TestEmail.send(
            statement,
            identifier=identifier,
            receiver=[self.user],
            template_name=bplan_emails.OfficeWorkerNotification.template_name,
        )

        TestEmail.send(
            statement,
            receiver=[self.user],
            template_name=bplan_emails.SubmitterConfirmation.template_name,
        )

    def _send_bplan_update(self):
        # Send notification for bplan update
        bplan = Bplan.objects.first()
        if not bplan:
            self.stderr.write("At least one bplan is required")
            return

        TestEmail.send(
            bplan,
            receiver=[self.user],
            template_name=bplan_emails.OfficeWorkerUpdateConfirmation.template_name,
        )

    def _send_report_mails(self):
        report = Report.objects.first()
        if not report:
            self.stderr.write("At least on report is required")
            return

        TestEmail.send(
            report,
            receiver=[self.user],
            template_name=reports_emails.ReportModeratorEmail.template_name,
        )

    def _send_invitation_private_project(self):
        invite = project_models.ParticipantInvite.objects.first()
        if not invite:
            self.stderr.write("At least one participant request is required")
            return
        TestEmail.send(
            invite,
            receiver=[self.user],
            template_name="meinberlin_projects/emails/invite_participant",
        )

    def _send_invitation_moderator(self):
        invite = project_models.ModeratorInvite.objects.first()
        if not invite:
            self.stderr.write("At least one moderator request is required")
            return
        TestEmail.send(
            invite,
            receiver=[self.user],
            template_name="meinberlin_projects/emails/invite_moderator",
        )

    def _send_initiator_request(self):
        organisation = Organisation.objects.first()
        TestEmail.send(
            self.user,
            organisation=organisation,
            phone="01234567",
            receiver=[self.user],
            template_name="meinberlin_initiators/emails/initiator_request",
        )

    def _send_welcome_email(self):
        TestEmail.send(
            self.user,
            receiver=[self.user],
            template_name="meinberlin_users/emails/welcome",
        )

    def _send_form_mail(self):
        emailformpage = EmailFormPage.objects.first()
        if not emailformpage:
            self.stderr.write("At least one emailformpage obj is required")
            return
        fields = {
            "Multi": "some text with \n" "newlines and \n" "such things",
            "Single": "just a single line of text that was entered",
            "More fields": "more text",
            "No more fields": "more text",
        }

        TestEmail.send(
            emailformpage,
            field_values=fields,
            receiver=[self.user],
            template_name="meinberlin_cms/emails/form_submission",
        )

    def _send_allauth_account_already_exists(self):
        context = {
            "user": self.user,
            "password_reset_url": "http://example.com/...",
        }

        TestEmail.send(
            self.user,
            receiver=[self.user],
            template_name="account/email/account_already_exists",
            **context
        )

    def _send_allauth_password_reset(self):
        context = {
            "user": self.user,
            "password_reset_url": "http://example.com/...",
            "request": None,
            "username": self.user.username,
        }

        TestEmail.send(
            self.user,
            receiver=[self.user],
            template_name="account/email/password_reset_key",
            **context
        )

    def _send_allauth_email_confirmation(self):
        context = {
            "user": self.user,
            "activate_url": "http://example.com/...",
            "key": "the1454key",
        }

        TestEmail.send(
            self.user,
            receiver=[self.user],
            template_name="account/email/email_confirmation_signup",
            **context
        )

        TestEmail.send(
            self.user,
            receiver=[self.user],
            template_name="account/email/email_confirmation",
            **context
        )

    def _send_allauth_unknown_account(self):
        context = {
            "user": self.user,
            "email": "user@example.com",
            "signup_url": "http://example.com/...",
        }

        TestEmail.send(
            self.user,
            receiver=[self.user],
            template_name="account/email/unknown_account",
            **context
        )
