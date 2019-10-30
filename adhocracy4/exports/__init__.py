import html

from django.utils.html import strip_tags


def unescape_and_strip_html(text):
    return strip_tags(html.unescape(text)).strip()
