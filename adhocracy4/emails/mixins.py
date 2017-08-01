from email.mime.image import MIMEImage

from django.contrib.staticfiles import finders
from .base import EmailBase


class PlatformEmailMixin:
    """
    Attaches the static file images/logo.png so it can be used in an html
    email.
    """
    def get_attachments(self):
        attachments = super().get_attachments()
        filename = finders.find('images/email_logo.png')
        if filename:
            f = open(filename, 'rb')
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<{}>'.format('logo'))
            return attachments + [logo]
        return attachments


class SyncEmailMixin(EmailBase):
    """Send Emails synchronously."""

    @classmethod
    def send(cls, object, *args, **kwargs):
        """Call dispatch immediately"""
        return cls().dispatch(object, *args, **kwargs)
