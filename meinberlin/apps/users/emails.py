from django.conf import settings

from adhocracy4.emails.mixins import SyncEmailMixin
from meinberlin.apps.contrib.emails import Email


class WelcomeEmail(SyncEmailMixin, Email):
    template_name = "meinberlin_users/emails/welcome"

    def get_receivers(self):
        receiver = self.object
        return [receiver]

    def get_context(self):
        context = super().get_context()
        context["contact_email"] = settings.CONTACT_EMAIL
        return context
