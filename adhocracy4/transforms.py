import bleach
from django.conf import settings


def clean_html_all(text):
    return bleach.clean(text,
                        tags=[], attributes={}, styles=[], strip=True)


def clean_html_field(text, setting='default'):
    allowed_tags = settings.BLEACH_LIST[setting]['tags']
    allowed_attrs = settings.BLEACH_LIST[setting]['attributes']
    allowed_styles = settings.BLEACH_LIST[setting].get('styles', [])
    return bleach.clean(text,
                        tags=allowed_tags,
                        attributes=allowed_attrs,
                        styles=allowed_styles,
                        strip=True)
