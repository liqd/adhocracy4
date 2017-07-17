import re

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

from adhocracy4.emails.mixins import SyncEmailMixin
from apps.contrib.emails import Email
from apps.users import USERNAME_INVALID_MESSAGE
from apps.users import USERNAME_REGEX


class UserAccountEmail(Email, SyncEmailMixin):
    def get_receivers(self):
        return [self.object]

    @property
    def template_name(self):
        return self.kwargs['template_name']

    def get_context(self):
        context = super().get_context()
        context['contact_email'] = settings.CONTACT_EMAIL
        return context


class AccountAdapter(DefaultAccountAdapter):
    username_regex = re.compile(USERNAME_REGEX)
    error_messages = dict(
        DefaultAccountAdapter.error_messages,
        invalid_username=USERNAME_INVALID_MESSAGE
    )

    def send_mail(self, template_prefix, email, context):
        user = context['user']
        return UserAccountEmail.send(
            user,
            template_name=template_prefix,
            **context
        )
