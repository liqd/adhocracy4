import re
from urllib.parse import quote

from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme

from adhocracy4.emails.mixins import SyncEmailMixin
from meinberlin.apps.contrib.emails import Email
from meinberlin.apps.users import USERNAME_INVALID_MESSAGE
from meinberlin.apps.users import USERNAME_REGEX
from meinberlin.apps.users.models import User


class UserAccountEmail(SyncEmailMixin, Email):
    def get_receivers(self):
        return [self.object]

    @property
    def template_name(self):
        return self.kwargs["template_name"]

    def get_context(self):
        context = super().get_context()
        context["contact_email"] = settings.CONTACT_EMAIL
        return context


class AccountAdapter(DefaultAccountAdapter):
    username_regex = re.compile(USERNAME_REGEX)
    error_messages = dict(
        DefaultAccountAdapter.error_messages, invalid_username=USERNAME_INVALID_MESSAGE
    )

    def get_email_confirmation_url(self, request, emailconfirmation):
        url = super().get_email_confirmation_url(request, emailconfirmation)
        if "next" in request.POST and url_has_allowed_host_and_scheme(
            request.POST["next"], allowed_hosts=None
        ):
            return "{}?next={}".format(url, quote(request.POST["next"]))
        else:
            return url

    def send_mail(self, template_prefix, email, context):
        context.update({"email": email})
        return UserAccountEmail.send(email, template_name=template_prefix, **context)

    def get_email_verification_redirect_url(self, email_address):
        if "next" in self.request.GET and url_has_allowed_host_and_scheme(
            self.request.GET["next"], allowed_hosts=None
        ):
            return self.request.GET["next"]
        else:
            return super().get_email_verification_redirect_url(email_address)

    def clean_username(self, username):
        username = super().clean_username(username)

        user = User.objects.filter(email__iexact=username)
        if user.exists():
            raise forms.ValidationError(
                User._meta.get_field("username").error_messages["used_as_email"]
            )

        return username
