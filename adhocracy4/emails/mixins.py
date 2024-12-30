from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import mail_admins


class PlatformEmailMixin:
    """
    Attaches the static file images/logo.png so it can be used in an html
    email.
    """

    def get_attachments(self):
        attachments = super().get_attachments()
        additional_files = getattr(
            settings,
            "A4_EMAIL_ATTACHMENTS",
            [
                ("logo", "images/email_logo.svg"),
                ("logo", "images/email_logo.png"),
            ],
        )
        files = []
        for identifier, file in additional_files:
            filename = finders.find(file)
            if filename:
                if filename.endswith(".png"):
                    imagetype = "png"
                else:
                    imagetype = "svg+xml"

                with open(filename, "rb") as f:
                    image = MIMEImage(f.read(), imagetype)

                image.add_header("Content-ID", "<{}>".format(identifier))
                files.append(image)
        return attachments + files


class SyncEmailMixin:
    """Send Emails synchronously."""

    @classmethod
    def send(cls, object, *args, **kwargs):
        """Call dispatch immediately"""
        return cls().dispatch(object, *args, **kwargs)


class ReportToAdminEmailMixin:

    enable_reporting = True
    report_subject_template = "{site}: {success} of {total} mails sended"
    report_message_template = """
Errors (if any):
{errors}

Mail sample:
{mail_sample}"""

    def handle_report(self, mails, mail_exceptions):
        mail_admins(
            subject=self.report_subject_template.format(
                site=self.get_site(),
                success=len(mails) - len(mail_exceptions),
                total=len(mails),
            ),
            message=self.report_message_template.format(
                errors="\n".join(str(i) for i in mail_exceptions),
                mail_sample=mails[0].message() if mails else None,
            ),
        )
