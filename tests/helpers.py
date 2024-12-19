import base64
import re
from io import BytesIO

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core import mail
from PIL import Image


class pytest_regex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(str(actual)))

    def __repr__(self):
        return self._regex.pattern


def clear_query_cache():
    """Clear the cache for GenericRelations.
    Required for django_assert_num_queries to work correctly, as otherwise
    some queries will be cached. Call directly before django_assert_num_queries."""
    ContentType.objects.clear_cache()
    Site.objects.clear_cache()


def get_emails_for_address_and_subject(email_address, subject):
    """Return all emails send to email_address with a subject starting with subject"""
    emails = list(
        filter(
            lambda mails: mails.to[0] == email_address and subject in mails.subject,
            mail.outbox,
        )
    )
    return emails


def get_base64_image(width, height):
    """Returns a base64 encoded jpeg image with the given width and height"""
    image = Image.new("RGB", size=(width, height), color=(256, 0, 0))
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())
