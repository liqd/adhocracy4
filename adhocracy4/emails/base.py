from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites import models as site_models
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import select_template
from django.utils import translation

from . import tasks


class EmailBase:
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

    def get_attachments(self):
        return []

    def get_languages(self, receiver):
        return [translation.get_language(), self.fallback_language]

    def get_reply_to(self):
        return None

    @classmethod
    def send(cls, object, *args, **kwargs):
        """Send email asynchronously.

        NOTE: args and kwargs must be JSON serializable.
        """
        ct = ContentType.objects.get_for_model(object)
        tasks.send_async(
            cls.__module__, cls.__name__,
            ct.app_label, ct.model, object.pk,
            args, kwargs)
        return []

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
                context['part_type'] = part_type
                parts.append(template.render(context))
                context.pop('part_type')

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
            context['receiver'] = receiver
            (subject, text, html) = self.render(template, context)
            context.pop('receiver')

            if hasattr(receiver, 'email'):
                to_address = receiver.email
            else:
                to_address = receiver

            mail = EmailMultiAlternatives(
                subject=subject.strip(),
                body=text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_address],
                reply_to=self.get_reply_to(),
            )

            if len(attachments) > 0:
                mail.mixed_subtype = 'related'

                for attachment in attachments:
                    mail.attach(attachment)

            mail.attach_alternative(html, 'text/html')
            mail.send()
            mails.append(mail)
        return mails
