from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

_extra_plugins = ['collapsibleItem', 'embed', 'embedbase']
_external_plugin_resources = [(
    'collapsibleItem',
    '/static/ckeditor_collapsible/',
    'plugin.js',
)]


class RichTextCollapsibleMixin:
    def __init__(self, *args, **kwargs):
        kwargs['extra_plugins'] = \
            kwargs.get('extra_plugins', []) + \
            _extra_plugins
        kwargs['external_plugin_resources'] = \
            kwargs.get('external_plugin_resources', []) \
            + _external_plugin_resources
        super().__init__(*args, **kwargs)


class RichTextCollapsibleField(RichTextCollapsibleMixin,
                               RichTextField):
    pass


class RichTextCollapsibleUploadingField(RichTextCollapsibleMixin,
                                        RichTextUploadingField):
    pass
