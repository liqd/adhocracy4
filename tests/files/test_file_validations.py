import pytest

from adhocracy4.files.validators import validate_file_type_and_size

from django.core.exceptions import ValidationError


def test_file_type_validation(image_factory):
    jpg_image = image_factory((100, 100), 'JPEG')
    gif_image = image_factory((100, 100), 'GIF')

    validate_file_type_and_size(
        jpg_image, {'fileformats': (('.jpg', 'image/jpeg'),)}
    )

    with pytest.raises(ValidationError):
        validate_file_type_and_size(gif_image, {
            'fileformats': (('.jpg', 'image/jpeg'),)
        })


def test_file_size_validation(image_factory):
    image = image_factory((100, 100), 'JPEG')

    with pytest.raises(ValidationError):
        validate_file_type_and_size(image, {
            'fileformats': (('.jpg', 'image/jpeg'),),
            'max_size': image.size - 1
        })
