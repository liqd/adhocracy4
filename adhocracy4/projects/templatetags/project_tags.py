from django import template
from django.utils.translation import gettext as _
from django.utils.translation import ngettext

register = template.Library()


@register.simple_tag
def get_days(number):
    # FIXME: only used in opin. Do we need it? Is there a better way?
    if number and number >= 1 and number <= 5:
        text = ngettext("%(number)d day left", "%(number)d days left", number) % {
            "number": number,
        }
        return text
    elif number == 0:
        return _("a few hours left")
    else:
        return ""


@register.simple_tag
def project_tile_image(project):
    return project.tile_image or project.image or None


@register.simple_tag
def project_tile_image_copyright(project):
    if project.tile_image:
        return project.tile_image_copyright
    elif project.image:
        return project.image_copyright
    else:
        return None
