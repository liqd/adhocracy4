import json

from django import template
from django_ckeditor_5.widgets import CKEditor5Widget
from rest_framework.renderers import JSONRenderer

from meinberlin.apps.documents.models import Chapter
from meinberlin.apps.documents.serializers import ChapterSerializer

register = template.Library()


@register.inclusion_tag("meinberlin_documents/react_documents.html", takes_context=True)
def react_documents(context, module, reload_on_success=False):
    chapters = Chapter.objects.filter(module=module)
    serializer = ChapterSerializer(chapters, many=True)
    chapters_json = JSONRenderer().render(serializer.data).decode("utf-8")

    widget = CKEditor5Widget(config_name="image-editor")
    config = JSONRenderer().render(widget.config).decode("utf-8")

    context = {
        "chapters": chapters_json,
        "module": module.pk,
        "config": config,
        "id": "document-" + str(module.id),
        "reload_on_success": json.dumps(reload_on_success),
        "ckeditor_media": widget.media,
    }

    return context
