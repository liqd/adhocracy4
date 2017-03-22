from email.mime.image import MIMEImage

from django.contrib.staticfiles import finders


class PlatformEmailMixin():
    """
    Attaches the static file images/logo.png so it can be used in an html
    email.
    """
    def get_attachments(self):
        attachments = super().get_attachments()
        filename = finders.find('images/logo.png')
        if filename:
            f = open(filename, 'rb')
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<{}>'.format('logo'))
            return attachments + [logo]
        return attachments
