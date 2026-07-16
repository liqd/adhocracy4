import pytest
from django.conf import settings
from django.core import mail

from adhocracy4.emails.base import EmailBase
from adhocracy4.emails.mixins import SyncEmailMixin
from adhocracy4.reports.emails import ReportModeratorEmail
from tests.reports.factories import ReportFactory


def test_get_from_email_defaults_to_settings():
    email = EmailBase()
    assert email.get_from_email() == settings.DEFAULT_FROM_EMAIL


class CustomFromEmail(SyncEmailMixin, EmailBase):
    template_name = ReportModeratorEmail.template_name

    def get_receivers(self):
        return [self.kwargs["receiver"]]

    def get_from_email(self):
        return "Custom Sender <custom@example.com>"


@pytest.mark.django_db
def test_dispatch_uses_get_from_email(user):
    report = ReportFactory()
    CustomFromEmail.send(report, receiver=user.email)

    assert len(mail.outbox) == 1
    assert mail.outbox[0].from_email == "Custom Sender <custom@example.com>"
