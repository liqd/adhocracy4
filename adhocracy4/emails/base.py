import re
from smtplib import SMTPException

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import select_template
from django.utils import translation

from . import tasks


class EmailBase:
    site_id = None
    object = None
    template_name = None
    for_moderator = False

    # will aggregate exceptions instead of raising them
    # then pass the exception with all mails to `handle_report`
    enable_reporting = False

    def get_site(self):
        if self.site_id is not None:
            return Site.objects.get(pk=self.site_id)
        elif hasattr(settings, 'SITE_ID'):
            return Site.objects.get(pk=settings.SITE_ID)
        else:
            return None

    def get_host(self):
        site = self.get_site()
        if site is None:
            return ''

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

    def get_fallback_language(self):
        if hasattr(settings, 'DEFAULT_LANGUAGE'):
            return settings.DEFAULT_LANGUAGE
        elif hasattr(settings, 'DEFAULT_USER_LANGUAGE_CODE'):
            return settings.DEFAULT_USER_LANGUAGE_CODE
        return 'en'

    def get_languages(self, receiver):
        return [translation.get_language(), self.get_fallback_language()]

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
        mail_exceptions = []
        for receiver in receivers:
            context['receiver'] = receiver
            (subject, text, html) = self.render(template, context)
            context.pop('receiver')

            if hasattr(receiver, 'email'):
                to_address = receiver.email
            else:
                to_address = receiver

            subject_clean = re.sub(r'[\r\n]', '', subject).strip()

            mail = EmailMultiAlternatives(
                subject=subject_clean,
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
            mails.append(mail)

            if self.enable_reporting:
                try:
                    mail.send()
                except SMTPException as exc:
                    mail_exceptions.append(exc)
            else:
                mail.send()

        if self.enable_reporting:
            self.handle_report(mails, mail_exceptions)

        return mails
