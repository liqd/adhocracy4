import pytest

from adhocracy4.images.validators import validate_image

from django.core.exceptions import ValidationError


def test_min_size_validation(image_factory):
    with pytest.raises(ValidationError):
        image = image_factory((100, 100), 'JPEG')
        validate_image(image, {'min_resolution': (50, 101)})

    with pytest.raises(ValidationError):
        image = image_factory((100, 100), 'JPEG')
        validate_image(image, {'min_resolution': (101, 50)})

    image = image_factory((100, 100), 'JPEG')
    validate_image(image, {'min_resolution': (100, 100)})


def test_aspect_validation(image_factory):
    square_image = image_factory((100, 109), 'JPEG')
    image = image_factory((100, 120), 'JPEG')

    validate_image(square_image, {'min_resolution': (100, 100),
                                  'aspect_ratio': (1, 1)})

    with pytest.raises(ValidationError):
        validate_image(image, {'min_resolution': (100, 100),
                               'aspect_ratio': (1, 1)})
