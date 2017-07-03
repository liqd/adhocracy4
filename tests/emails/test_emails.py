import importlib
from unittest.mock import patch

import pytest
from django.core import mail

from adhocracy4.emails import EmailBase

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
    send_emails = EmailTest.send(user)

    assert len(mail.outbox) == 1
    assert mail.outbox[0] == send_emails[0]
    assert mail.outbox[0].subject == CONTEXT['subject']


@pytest.mark.django_db
def test_send_async(user):
    # Patch the background task decorator and reload the module
    patch('background_task.background',
          wraps=lambda **kwargs: lambda f: f).start()
    import adhocracy4.emails.tasks
    importlib.reload(adhocracy4.emails.tasks)

    send_async_mails = EmailTest.send_async(user)

    assert send_async_mails == []
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == CONTEXT['subject']
