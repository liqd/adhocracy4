import json

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import template
from rest_framework.renderers import JSONRenderer

from apps.documents.models import Chapter
from apps.documents.serializers import ChapterSerializer

register = template.Library()


@register.inclusion_tag('meinberlin_documents/react_documents.html',
                        takes_context=True)
def react_documents(context, module):
    chapters = Chapter.objects.filter(module=module)
    serializer = ChapterSerializer(chapters, many=True)
    chapters_json = JSONRenderer().render(serializer.data)

    widget = CKEditorUploadingWidget(config_name='image-editor')
    widget._set_config()
    config = widget.config

    context = {
        'chapters': chapters_json,
        'module': module.pk,
        'config': json.dumps(config),
        'id': 'document-' + str(module.id)
    }

    return context
