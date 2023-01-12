import bleach
from bleach.css_sanitizer import CSSSanitizer
from django.conf import settings


def clean_html_all(text):
    css_sanitizer = CSSSanitizer(allowed_css_properties=[])
    return bleach.clean(
        text, tags=[], attributes={}, css_sanitizer=css_sanitizer, strip=True
    )


def clean_html_field(text, setting="default"):
    css_sanitizer = CSSSanitizer(
        allowed_css_properties=settings.BLEACH_LIST[setting].get("styles", [])
    )
    allowed_tags = settings.BLEACH_LIST[setting]["tags"]
    allowed_attrs = settings.BLEACH_LIST[setting]["attributes"]
    return bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attrs,
        css_sanitizer=css_sanitizer,
        strip=True,
    )
