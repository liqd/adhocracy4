import json

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import template
from rest_framework.renderers import JSONRenderer

from apps.documents.serializers import ChapterSerializer

register = template.Library()


@register.inclusion_tag('meinberlin_documents/react_paragraphs.html',
                        takes_context=True)
def react_paragraphs(context, doc, module):

    serializer = ChapterSerializer(doc)
    chapter = JSONRenderer().render(serializer.data)
    widget = CKEditorUploadingWidget(config_name='image-editor')
    widget._set_config()
    config = widget.config

    if doc is None:
        _id = None
    else:
        _id = 'paragraphs-' + str(doc.pk)

    context = {
        'chapter': chapter,
        'module': module.pk,
        'config': json.dumps(config),
        'id': _id
    }

    return context
