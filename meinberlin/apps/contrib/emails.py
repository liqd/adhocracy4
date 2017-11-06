from django.conf import settings

from adhocracy4 import emails as a4_emails


class Email(a4_emails.Email):
    """Email base class with a configurable default language."""

    fallback_language = 'en'

    def get_languages(self, receiver):
        return [settings.DEFAULT_LANGUAGE, self.fallback_language]
