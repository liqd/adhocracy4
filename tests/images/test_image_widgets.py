from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.safestring import SafeData

from adhocracy4.images import widgets


def test_render_empty():
    input = widgets.ImageInputWidget()
    html = input.render('image_name', None)

    assert isinstance(html, SafeData)


def test_image_input_delete_presedence():
    input = widgets.ImageInputWidget()
    jpeg_file = SimpleUploadedFile('test.jpg', b'file content',
                                   content_type='image/jpeg')

    data = {'test_image-clear': 'on'}
    files = {'test_image': jpeg_file}
    value = input.value_from_datadict(data, files, 'test_image')
    assert value is False

    value = input.value_from_datadict(data, {}, 'test_image')
    assert value is False

    value = input.value_from_datadict({}, files, 'test_image')
    assert value is jpeg_file
