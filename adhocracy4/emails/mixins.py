from email.mime.image import MIMEImage

from django.contrib.staticfiles import finders
from django.utils.translation import get_language
from django.template.loader import select_template


class SingleTemplateMixin():
    def render(self, template_name, context):
        languages = [get_language(), self.fallback_language]
        template = select_template([
            'emails/{}.{}.email'.format(template_name, lang)
            for lang in languages
        ])

        parts = []
        for part_type in ('subject', 'txt', 'html'):
            context.update({'part_type': part_type})
            parts.append(template.render(context))
            context.pop()

        return tuple(parts)


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
