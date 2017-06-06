import json

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import template
from rest_framework.renderers import JSONRenderer

from apps.documents.serializers import ChapterSerializer

register = template.Library()


@register.inclusion_tag('meinberlin_documents/react_paragraphs.html',
                        takes_context=True)
def react_paragraphs(context, chapter, module):

    serializer = ChapterSerializer(chapter)
    chapter_json = JSONRenderer().render(serializer.data)
    widget = CKEditorUploadingWidget(config_name='image-editor')
    widget._set_config()
    config = widget.config

    if chapter is None:
        _id = None
    else:
        _id = 'paragraphs-' + str(chapter.pk)

    context = {
        'chapter': chapter_json,
        'module': module.pk,
        'config': json.dumps(config),
        'id': _id
    }

    return context
