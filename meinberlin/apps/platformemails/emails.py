from allauth.account.models import EmailAddress
from django.contrib import auth

from adhocracy4.emails.mixins import ReportToAdminEmailMixin
from meinberlin.apps.contrib.emails import Email

User = auth.get_user_model()


class PlatformEmail(ReportToAdminEmailMixin, Email):
    template_name = "meinberlin_platformemails/emails/platform_email"

    def get_reply_to(self):
        return ["{} <{}>".format(self.object.sender_name, self.object.sender)]

    def get_receivers(self):
        verified_emails = EmailAddress.objects.filter(verified=True).values("email")
        return (
            User.objects.filter(is_active=True)
            .filter(email__in=verified_emails)
            .distinct()
        )
