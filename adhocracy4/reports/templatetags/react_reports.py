import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils.translation import ugettext as _

register = template.Library()


@register.simple_tag
def react_reports(obj, text=None, **kwargs):
    contenttype = ContentType.objects.get_for_model(obj)

    mountpoint = 'report_for_{contenttype}_{pk}'.format(
        contenttype=contenttype.pk,
        pk=obj.pk
    )

    modal_name = '{mountpoint}_modal'.format(mountpoint=mountpoint)

    attributes = {
        'contentType': contenttype.pk,
        'objectId': obj.pk,
        'modalName': modal_name,
    }

    if text is None:
        text = _('Report')

    if 'class' in kwargs:
        class_names = kwargs['class']

    return format_html(
        (
            '<a href="#{modal_name}" data-a4-widget="reports"'
            ' data-attributes="{attributes}" class="{class_names}">{text}</a>'
        ),
        attributes=json.dumps(attributes),
        modal_name=modal_name,
        class_names=class_names,
        text=text,
    )
