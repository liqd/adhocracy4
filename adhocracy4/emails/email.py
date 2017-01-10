from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.sites import models as site_models
from django.contrib.staticfiles import finders
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import select_template
from django.utils.translation import get_language


class Email:
    site_id = 1
    object = None
    template_name = None
    fallback_language = 'en'
    for_moderator = False

    def get_site(self):
        return site_models.Site.objects.get(pk=self.site_id)

    def get_host(self):
        site = self.get_site()
        ssl_enabled = True
        if site.domain.startswith('localhost:'):
            ssl_enabled = False

        url = 'http{ssl_flag}://{domain}'.format(
            ssl_flag='s' if ssl_enabled else '',
            domain=site.domain,
        )
        return url

    def get_context(self):
        object_context_key = self.object.__class__.__name__.lower()
        return {
            'email': self,
            'site': self.get_site(),
            object_context_key: self.object
        }

    def get_receivers(self):
        return []

    def get_receiver_emails(self):
        return [receiver.email for receiver in self.get_receivers()]

    def get_attachments(self):
        return []

    @classmethod
    def send(cls, obj, **kwargs):
        return cls().dispatch(obj, **kwargs)

    def dispatch(self, obj, **kwargs):
        self.object = obj
        languages = [get_language(), self.fallback_language]
        receivers = self.get_receiver_emails()
        context = self.get_context()
        context.update(kwargs)
        attachments = self.get_attachments()
        template = self.template_name

        subject = select_template([
            'emails/{}.{}.subject'.format(template, lang) for lang in languages
        ])
        plaintext = select_template([
            'emails/{}.{}.txt'.format(template, lang) for lang in languages
         ])
        html = select_template([
            'emails/{}.{}.html'.format(template, lang) for lang in languages
        ])
        mail = EmailMultiAlternatives(
            subject=subject.render(context).strip(),
            body=plaintext.render(context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=receivers,
        )
        if len(attachments) > 0:
            mail.mixed_subtype = 'related'

            for attachment in attachments:
                mail.attach(attachment)

        mail.attach_alternative(html.render(context), 'text/html')
        mail.send()
        return mail


class ExternalNotification(Email):
    email_attr_name = 'email'

    def get_receiver_emails(self):
        return [getattr(self.object, self.email_attr_name)]

    def get_context(self):
        context = super().get_context()
        context['receiver'] = getattr(self.object, self.email_attr_name)
        return context


class UserNotification(Email):
    user_attr_name = 'creator'

    def get_receivers(self):
        return [getattr(self.object, self.user_attr_name)]

    def get_context(self):
        context = super().get_context()
        context['receiver'] = getattr(self.object, self.user_attr_name)
        return context


class ModeratorNotification(Email):
    def get_receivers(self):
        return self.object.project.moderators.all()


class InitiatorNotification(Email):
    def get_receivers(self):
        return self.object.organisation.initiators.all()


def send_email_with_template(receivers, template, additional_context):

    class EmailWithTemplate(Email):
        template_name = template

        def get_receiver_emails(self):
            return receivers

        def get_attachments(self):
            attachments = super().get_attachments()
            filename = finders.find('images/logo.png')
            if filename:
                f = open(filename, 'rb')
                logo = MIMEImage(f.read())
                logo.add_header('Content-ID', '<{}>'.format('logo'))
                return attachments + [logo]
            return attachments

        def get_context(self):
            context = super().get_context()
            context.update({
                'site': self.get_site(),
            })
            context.update(dict(additional_context))
            return context

    EmailWithTemplate.send(None)
