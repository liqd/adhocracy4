import pytest
from django.core.exceptions import ValidationError

from adhocracy4.images.validators import validate_image


def test_min_size_validation(image_factory):
    with pytest.raises(ValidationError):
        image = image_factory((100, 100), 'JPEG')
        validate_image(image, (50, 101))

    with pytest.raises(ValidationError):
        image = image_factory((100, 100), 'JPEG')
        validate_image(image, (101, 50))

    image = image_factory((100, 100), 'JPEG')
    validate_image(image, (100, 100))


def test_aspect_validation(image_factory):
    square_image = image_factory((100, 109), 'JPEG')
    image = image_factory((100, 120), 'JPEG')

    validate_image(square_image, (100, 100), aspect_ratio=(1, 1))

    with pytest.raises(ValidationError):
        validate_image(image, (100, 100), aspect_ratio=(1, 1))


def test_file_type_validation(image_factory):
    jpg_image = image_factory((100, 100), 'JPEG')
    gif_image = image_factory((100, 100), 'GIF')

    validate_image(
        jpg_image, (100, 100),
        fileformats=('image/jpeg')
    )

    with pytest.raises(ValidationError):
        validate_image(gif_image, (100, 100), fileformats=('image/jpeg'))


def test_file_size_validation(image_factory):
    image = image_factory((100, 100), 'JPEG')

    with pytest.raises(ValidationError):
        validate_image(image, (100, 100), max_size=image.size - 1)
