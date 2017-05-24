import re
import unicodedata

from django import template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def classify(value):
    """
    Create a valid CSS class name from a value.

    Converts to ASCII. Converts spaces to dashes. Removes characters that
    aren't alphanumerics, underscores, or hyphens.
    Also strips leading and trailing whitespace.
    """
    if value is None:
        return 'NONE'

    value = force_text(value)
    value = unicodedata.normalize('NFKD', value) \
        .encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip()
    return mark_safe(re.sub('[-\s]+', '-', value))
