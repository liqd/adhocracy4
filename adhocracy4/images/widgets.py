from django.utils.translation import ugettext_lazy as _

from adhocracy4.files.widgets import FileInputWidget


class ImageInputWidget(FileInputWidget):

    """
    A project-specific improved version of the clearable file upload.

    Allows to upload and delete uploaded files. It doesn't passing attributes
    using the positional `attrs` argument and hard codes css files.
    """
    class Media:
        js = ('a4images/imageUploader.js',)

    file_placeholder = _('Select a picture from your local folder.')
    template_name = 'a4images/image_upload_widget.html'
