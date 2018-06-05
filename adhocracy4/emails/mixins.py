from email.mime.image import MIMEImage

from django.contrib.staticfiles import finders
from django.db.transaction import atomic

from adhocracy4.emails.tasks import send_single_mail


class PlatformEmailMixin:
    """
    Attaches the static file images/logo.png so it can be used in an html
    email.
    """

    def get_attachments(self):
        attachments = super().get_attachments()
        filename = (finders.find('images/email_logo.png')
                    or finders.find('images/email_logo.svg'))
        if filename:
            if filename.endswith('.png'):
                imagetype = 'png'
            else:
                imagetype = 'svg+xml'

            with open(filename, 'rb') as f:
                logo = MIMEImage(f.read(), imagetype)

            logo.add_header('Content-ID', '<{}>'.format('logo'))
            return attachments + [logo]
        return attachments


class SyncEmailMixin:
    """Send Emails synchronously."""

    @classmethod
    def send(cls, object, *args, **kwargs):
        """Call dispatch immediately"""
        return cls().dispatch(object, *args, **kwargs)


class ParallelEmailMixin:
    def send_mail(self, mail):
        send_single_mail(
            mail, creator=self.object, verbose_name=' '.join(mail.to))

    # make all emails to be registered to the task queue atomically
    @atomic
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
