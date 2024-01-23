import math

import magic
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

image_max_mb = 5


def validate_image(
    image,
    min_resolution,
    max_size=image_max_mb * 10**6,
    fileformats=("image/png", "image/jpeg"),
    aspect_ratio=None,
    aspect_marign=0.1,
    max_resolution=None,
):
    errors = []
    min_width, min_height = min_resolution

    imagetype = magic.from_buffer(image.read(), mime=True)

    if imagetype.lower() not in fileformats:
        msg = _(
            "Unsupported file format. Supported formats are {}.".format(
                ", ".join(fileformats)
            )
        )
        raise ValidationError(msg)
    if image.size > max_size:
        max_size_mb = math.floor(max_size / 10**6)
        msg = _("Image should be at most {max_size} MB")
        errors.append(ValidationError(msg.format(max_size=max_size_mb)))

    if hasattr(image, "width"):
        image_width = image.width
    else:
        image_width = image.image.width
    if image_width < min_width:
        msg = _("Image must be at least {min_width} pixels wide")
        errors.append(ValidationError(msg.format(min_width=min_width)))

    if hasattr(image, "height"):
        image_height = image.height
    else:
        image_height = image.image.height
    if image_height < min_height:
        msg = _("Image must be at least {min_height} pixels high")
        errors.append(ValidationError(msg.format(min_height=min_height)))

    if max_resolution:
        max_width, max_height = max_resolution
        if image_width > max_width:
            msg = _("Image must be at most {max_width} pixels wide")
            errors.append(ValidationError(msg.format(max_width=max_width)))
        if image_height > max_height:
            msg = _("Image must be at most {max_height} pixels high")
            errors.append(ValidationError(msg.format(max_height=max_height)))

    if aspect_ratio:
        aspect_heigth, aspect_width = aspect_ratio
        target_ratio = aspect_heigth / aspect_width
        actual_ratio = image_height / image_width

        if abs(target_ratio - actual_ratio) > aspect_marign:
            msg = _("Image aspect ratio should be {aspect_width}:{aspect_height}")
            errors.append(
                ValidationError(
                    msg.format(aspect_width=aspect_width, aspect_height=aspect_heigth)
                )
            )

    if errors:
        raise ValidationError(errors)
    return image


@deconstructible
class ImageAltTextValidator:
    """Validate that if the input contains html img tags that all have the alt
    attribute set, otherwise raise ValidationError.
    """

    message = _("Please add an alternative text for all images.")
    code = "invalid"

    def __init__(self):
        pass

    def __call__(self, value):
        """Parse value with BeautifulSoup and check
        if img tags exist which don't have the alt attribute set"""

        soup = BeautifulSoup(value, "html.parser")
        img_tags = soup("img", alt=False)
        if len(img_tags) > 0:
            raise ValidationError(message=self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, ImageAltTextValidator)
            and self.message == other.message
            and self.code == other.code
        )
