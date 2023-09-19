from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# FIXME: remove these fields / file
class RichTextCollapsibleMixin:
    pass


class RichTextCollapsibleField(RichTextCollapsibleMixin, RichTextField):
    pass


class RichTextCollapsibleUploadingField(
    RichTextCollapsibleMixin, RichTextUploadingField
):
    pass
