from django.conf import settings
from django.template.loader import select_template
from django.utils import translation

from adhocracy4 import emails as a4_emails


class Email(a4_emails.Email):
    """Email base class with a configurable default language."""

    fallback_language = 'en'

    def render(self, template_name, context):
        languages = [settings.EMAIL_DEFAULT_LANGUAGE, self.fallback_language]
        template = select_template([
            '{}.{}.email'.format(template_name, lang)
            for lang in languages
        ])

        language = template.template.name.split('.', 2)[-2]

        with translation.override(language):
            parts = []
            for part_type in ('subject', 'txt', 'html'):
                context.update({'part_type': part_type})
                parts.append(template.render(context))
                context.pop()

        return tuple(parts)
