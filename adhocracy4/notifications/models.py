from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from adhocracy4.actions.verbs import Verbs

NOTIFIABLES = (
    "item",
    "comment",
    "rating",
)


class NotificationManager(models.Manager):

    def create_from_action(self, action, search_profiles=None):
        notifications = []
        verb = Verbs(action.verb)

        # For published projects, notify search profile creators.
        if verb == Verbs.PUBLISH and search_profiles:
            notifications = [
                Notification(
                    recipient=profile.creator, action=action, search_profile=profile
                )
                for profile in search_profiles
            ]

        # For create/add actions where the target has a creator.
        elif (
            hasattr(action.target, "creator")
            and verb in (Verbs.CREATE, Verbs.ADD)
            and (
                (
                    action.type in NOTIFIABLES
                    and action.target.creator.notification_settings.track_creator
                )
                or (
                    action.type == "moderatorremark"
                    and action.target.creator.notification_settings.track_creator_on_moderator_feedback
                )
            )
        ):
            notifications = [
                Notification(recipient=action.target.creator, action=action)
            ]

        # For phase and offlineevent notifications
        elif action.type in ("phase", "offlineevent"):
            User = get_user_model()
            followers = User.objects.filter(
                follow__project=action.project,
                follow__enabled=True,
            )

            recipients = []
            if (
                action.type == "phase"
                and action.project.project_type == "a4projects.Project"
            ):
                if verb == Verbs.START:
                    recipients = followers.filter(
                        notification_settings__track_followers_phase_started=True
                    )
                elif verb == Verbs.SCHEDULE:
                    recipients = followers.filter(
                        notification_settings__track_followers_phase_over_soon=True
                    )
            elif action.type == "offlineevent" and verb == Verbs.START:
                recipients = followers.filter(
                    notification_settings__track_followers_event_upcoming=True
                )

            notifications = [
                Notification(recipient=recipient, action=action)
                for recipient in recipients
            ]

        if notifications:
            created_objs = self.bulk_create(notifications)
            return len(created_objs)

        return 0


class Notification(models.Model):
    objects = NotificationManager()

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    action = models.ForeignKey(
        "a4actions.action", on_delete=models.CASCADE, related_name="+"
    )
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.recipient} regarding {self.action}"

    @classmethod
    def should_notify(cls, action):
        verb = Verbs(action.verb)

        if (
            hasattr(action.target, "creator")
            and action.type in NOTIFIABLES + ("moderatorremark",)
            and verb in (Verbs.CREATE, Verbs.ADD)
        ):
            return True

        if verb == Verbs.PUBLISH:
            return True

        if (
            action.type == "phase"
            and action.project.project_type == "a4projects.Project"
        ):
            if verb in (Verbs.START, Verbs.SCHEDULE):
                return True

        if action.type == "offlineevent" and verb == Verbs.START:
            return True

        return False


class NotificationSettings(models.Model):
    email_fields = [
        "email_newsletter",
        "notify_followers_phase_started",
        "notify_followers_phase_over_soon",
        "notify_followers_event_upcoming",
        "notify_creator",
        "notify_creator_on_moderator_feedback",
        "notify_initiators_project_created",
        "notify_moderator",
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_settings",
    )
    email_newsletter = models.BooleanField(default=False)

    """
    Notification fields are being used to check if a notification should be sent
    via email.
    """
    notify_followers_phase_started = models.BooleanField(default=True)
    notify_followers_phase_over_soon = models.BooleanField(default=True)
    notify_followers_event_upcoming = models.BooleanField(default=True)
    notify_creator = models.BooleanField(default=True)
    notify_creator_on_moderator_feedback = models.BooleanField(default=True)
    notify_initiators_project_created = models.BooleanField(default=True)
    notify_moderator = models.BooleanField(default=True)

    """
    Tracked fields are being used to check if a notification should show in
    the activity feed.
    """
    track_followers_phase_started = models.BooleanField(default=True)
    track_followers_phase_over_soon = models.BooleanField(default=True)
    track_followers_event_upcoming = models.BooleanField(default=True)
    track_creator = models.BooleanField(default=True)
    track_creator_on_moderator_feedback = models.BooleanField(default=True)

    def update_all_settings(self, notifications_on, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.BooleanField):
                if field.name in kwargs:
                    setattr(self, field.name, kwargs[field.name])
                else:
                    setattr(self, field.name, notifications_on)
        self.save()

    def update_email_settings(self, notifications_on, **kwargs):
        for field in self.email_fields:
            if field in kwargs:
                setattr(self, field, kwargs[field])
            else:
                setattr(self, field, notifications_on)
        self.save()
