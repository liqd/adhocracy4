from django.core.exceptions import ValidationError
from django.test.utils import override_settings
import pytest

from adhocracy4.images.validators import validate_image


@override_settings(ALLOWED_UPLOAD_IMAGES=('image/jpeg'))
def test_min_size_validation(image_factory):
    with pytest.raises(ValidationError):
        image = image_factory((100, 100), 'JPEG')
        validate_image(image, 50, 101)

    with pytest.raises(ValidationError):
        image = image_factory((100, 100), 'JPEG')
        validate_image(image, 101, 50)

    image = image_factory((100, 100), 'JPEG')
    validate_image(image, 100, 100)


@override_settings(ALLOWED_UPLOAD_IMAGES=('image/jpeg'))
def test_aspect_validation(image_factory):
    square_image = image_factory((100, 109), 'JPEG')
    image = image_factory((100, 120), 'JPEG')

    validate_image(square_image, 100, 100, (1, 1))

    with pytest.raises(ValidationError):
        validate_image(image, 100, 100, (1, 1))
