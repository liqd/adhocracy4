import pytest
from django.core import mail

from adhocracy4.emails import EmailBase
from adhocracy4.test.helpers import skip_background_mail

CONTEXT = {
    'subject': 'TEST SUBJECT',
    'headline': 'TEST HEADLINE',
    'content': 'TEST CONTENT',
    'cta_url': 'http://cta.url/',
    'cta_label': 'CTA LABEL',
    'reason': 'REASON'
}


class EmailTest(EmailBase):
    template_name = 'tests/emails/email_test'

    def get_languages(self, receiver):
        return ['en']

    def get_context(self):
        context = super().get_context()
        context.update(CONTEXT)
        return context

    def get_receivers(self):
        return [self.object]


@pytest.mark.django_db
def test_send_sync(user):
    send_emails = EmailTest.send_sync(user)

    assert len(mail.outbox) == 1
    assert mail.outbox[0] == send_emails[0]
    assert mail.outbox[0].subject == CONTEXT['subject']


@pytest.mark.django_db
def test_send_async(user):
    with skip_background_mail():
        send_async_mails = EmailTest.send(user)

    assert send_async_mails == []
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == CONTEXT['subject']
