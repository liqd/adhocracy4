from django import template
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

register = template.Library()


@register.simple_tag
def get_days(number):
    if number and number >= 1 and number <= 5:
        text = ungettext(
            '%(number)d day left',
            '%(number)d days left',
            number) % {
            'number': number,
        }
        return text
    elif number == 0:
        return _('a few hours left')
    else:
        return ''


@register.simple_tag
def get_class(project):
    if project.is_private:
        return 'private'
    elif project.has_finished:
        return 'finished'
    elif project.days_left and project.days_left <= 5:
        return 'running-out'
    elif project.is_semipublic:
        return 'semipublic'
    else:
        return 'public'


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
