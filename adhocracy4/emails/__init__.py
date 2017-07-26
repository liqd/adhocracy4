from django.conf import settings
from django.contrib.sites import models as site_models
from django.core.mail.message import EmailMultiAlternatives
from django.template import Context
from django.template.loader import select_template
from django.utils import translation

from . import mixins


class EmailBase:
    site_id = 1
    object = None
    template_name = None
    fallback_language = 'en'
    for_moderator = False

    def get_reply_to(self):
        return []

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
        return Context({
            'email': self,
            'site': self.get_site(),
            object_context_key: self.object
        })

    def get_receivers(self):
        return []

    def get_attachments(self):
        return []

    def get_languages(self, receiver):
        return [translation.get_language(), self.fallback_language]

    @classmethod
    def send(cls, object, *args, **kwargs):
        return cls().dispatch(object, *args, **kwargs)

    def render(self, template_name, context):
        languages = self.get_languages(context['receiver'])
        template = select_template([
            '{}.{}.email'.format(template_name, lang)
            for lang in languages
        ])

        # Get the actually chosen language from the template name
        language = template.template.name.split('.', 2)[-2]

        with translation.override(language):
            parts = []
            for part_type in ('subject', 'txt', 'html'):
                context.update({'part_type': part_type})
                parts.append(template.render(context))
                context.pop()

        return tuple(parts)

    def dispatch(self, object, *args, **kwargs):
        self.object = object
        self.kwargs = kwargs
        receivers = self.get_receivers()
        context = self.get_context()
        context.update(kwargs)
        attachments = self.get_attachments()
        template = self.template_name

        mails = []
        for receiver in receivers:
            context.update({'receiver': receiver})
            (subject, text, html) = self.render(template, context)
            context.pop()

            if hasattr(receiver, 'email'):
                to_address = receiver.email
            else:
                to_address = receiver

            mail = EmailMultiAlternatives(
                subject=subject.strip(),
                body=text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_address],
                reply_to=self.get_reply_to()
            )

            if len(attachments) > 0:
                mail.mixed_subtype = 'related'

                for attachment in attachments:
                    mail.attach(attachment)

            mail.attach_alternative(html, 'text/html')
            mail.send()
            mails.append(mail)
        return mails


class Email(mixins.PlatformEmailMixin, EmailBase):
    pass


class ExternalNotification(Email):
    email_attr_name = 'email'

    def get_receivers(self):
        return [getattr(self.object, self.email_attr_name)]


class UserNotification(Email):
    user_attr_name = 'creator'

    def get_receivers(self):
        return [getattr(self.object, self.user_attr_name)]


class ModeratorNotification(Email):
    def get_receivers(self):
        return self.object.project.moderators.all()


class InitiatorNotification(Email):
    def get_receivers(self):
        return self.object.organisation.initiators.all()
