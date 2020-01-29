from os.path import basename

from django.forms import widgets
from django.template import loader
from django.utils.html import conditional_escape
from django.utils.translation import ugettext


class ImageInputWidget(widgets.ClearableFileInput):

    """
    A project-specific improved version of the clearable file upload.

    Allows to upload and delete uploaded files. It doesn't passing attributes
    using the positional `attrs` argument and hard codes css files.
    """
    class Media:
        js = ('image_uploader.js'),

    def render(self, name, value, attrs=None, renderer=None):
        html_id = attrs and attrs.get('id', name) or name
        has_image_set = self.is_initial(value)
        is_required = self.is_required

        file_placeholder = ugettext('Select a picture from your local folder.')
        file_input = super().render(name, None, {
            'id': html_id,
            'class': 'form-control form-control-file'
        })

        if has_image_set:
            file_name = basename(value.name)
            file_url = conditional_escape(value.url)
        else:
            file_name = ""
            file_url = ""

        text_input = widgets.TextInput().render('__noname__', file_name, {
            'class': 'form-control form-control-file-dummy',
            'placeholder': file_placeholder,
            'tabindex': '-1',
            'id': 'text-{}'.format(html_id)
        })

        checkbox_id = self.clear_checkbox_id(name)
        checkbox_name = self.clear_checkbox_name(name)
        checkbox_input = widgets.CheckboxInput().render(checkbox_name, False, {
            'id': checkbox_id,
            'class': 'clear-image',
            'data-upload-clear': html_id,
        })

        context = {
            'id': html_id,
            'has_image_set': has_image_set,
            'is_required': is_required,
            'file_url': file_url,
            'file_input': file_input,
            'file_id': html_id + '-file',
            'text_input': text_input,
            'checkbox_input': checkbox_input,
            'checkbox_id': checkbox_id
        }

        return loader.render_to_string(
            'a4images/image_upload_widget.html',
            context
        )

    def value_from_datadict(self, data, files, name):
        """
        Modify value_from_datadict, so that delete takes precedence over
        upload.
        """
        file_value = super(widgets.ClearableFileInput, self)\
            .value_from_datadict(data, files, name)
        checkbox_value = widgets.CheckboxInput()\
            .value_from_datadict(data, files, self.clear_checkbox_name(name))
        if not self.is_required and checkbox_value:
            return False
        return file_value
