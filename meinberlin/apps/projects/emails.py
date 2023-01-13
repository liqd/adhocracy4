from django.conf import settings

from meinberlin.apps.contrib.emails import Email


class InviteParticipantEmail(Email):
    template_name = "meinberlin_projects/emails/invite_participant"

    def get_receivers(self):
        return [self.object.email]

    def get_context(self):
        context = super().get_context()
        context["contact_email"] = settings.CONTACT_EMAIL
        return context


class InviteModeratorEmail(Email):
    template_name = "meinberlin_projects/emails/invite_moderator"

    def get_receivers(self):
        return [self.object.email]

    def get_context(self):
        context = super().get_context()
        context["contact_email"] = settings.CONTACT_EMAIL
        return context
