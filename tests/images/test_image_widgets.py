from django.core.files.uploadedfile import SimpleUploadedFile

from adhocracy4.images import widgets


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
