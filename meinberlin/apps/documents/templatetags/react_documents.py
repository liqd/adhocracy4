import json

from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html
from django_ckeditor_5.widgets import CKEditor5Widget

from meinberlin.apps.documents.models import Chapter
from meinberlin.apps.documents.serializers import ChapterSerializer

register = template.Library()


@register.simple_tag()
def react_documents(module, reload_on_success=False):
    chapters = Chapter.objects.filter(module=module)
    serializer = ChapterSerializer(chapters, many=True)
    widget = CKEditor5Widget(config_name="image-editor")

    attributes = {
        "key": module.pk,
        "chapters": serializer.data,
        "module": module.pk,
        "config": widget.config,
        "csrfCookieName": settings.CSRF_COOKIE_NAME,
        "uploadUrl": reverse("ck_editor_5_upload_file"),
        "uploadFileTypes": settings.CKEDITOR_5_UPLOAD_FILE_TYPES,
        "id": "document-" + str(module.id),
        "reloadOnSuccess": reload_on_success,
    }

    return format_html(
        '<div data-mb-widget="document-management" '
        'data-attributes="{attributes}"></div>',
        attributes=json.dumps(attributes),
    )
