from email.mime.image import MIMEImage

from django.contrib import auth
from django.contrib.staticfiles import finders

from meinberlin.apps.contrib.emails import Email

User = auth.get_user_model()


class NewsletterEmail(Email):
    template_name = 'meinberlin_newsletters/emails/newsletter_email'

    def get_reply_to(self):
        return ['{} <{}>'.format(self.object.sender_name, self.object.sender)]

    def get_languages(self, receiver):
        return ['raw']

    def get_receivers(self):
        return User.objects.filter(id__in=self.kwargs['participant_ids'])

    def get_attachments(self):
        attachments = super().get_attachments()

        organisation = self.kwargs['organisation']
        if organisation.logo:
            f = open(organisation.logo.path, 'rb')
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<{}>'.format('logo'))
            attachments += [logo]
        meinberlin_filename = finders.find('images/email_logo.png')
        if meinberlin_filename:
            f = open(meinberlin_filename, 'rb')
            meinberlin_logo = MIMEImage(f.read())
            meinberlin_logo.add_header(
                'Content-ID', '<{}>'.format('meinberlin_logo'))
            attachments += [meinberlin_logo]

        return attachments
