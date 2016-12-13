import magic

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

image_max_mb = 5


def validate_image(image, min_width, min_height, aspect_ratio=None, aspect_marign=0.1):
    errors = []

    imagetype = magic.from_buffer(image.read(), mime=True)
    if imagetype.lower() not in settings.ALLOWED_UPLOAD_IMAGES:
        _msg = _("Unsupported file format. Supported formats are %s."
                                          % ", ".join(settings.ALLOWED_UPLOAD_IMAGES))
        errors.append(ValidationError(_msg))
    image_max_size = image_max_mb * 10**6
    if image.size > image_max_size:
        msg = _('Image should be at most {max_size} MB')
        errors.append(ValidationError(msg.format(max_size=image_max_mb)))
    if image.width < min_width:
        msg = _('Image must be at least {min_width} pixels wide')
        errors.append(ValidationError(msg.format(min_width=min_width)))
    if image.height < min_height:
        msg = _('Image must be at least {min_height} pixels high')
        errors.append(ValidationError(msg.format(min_height=min_height)))

    if aspect_ratio:
        aspect_heigth, aspect_width = aspect_ratio
        target_ratio = aspect_heigth/aspect_width
        actual_ratio = image.height/image.width

        if abs(target_ratio - actual_ratio) > aspect_marign:
            msg = _('Image aspect ratio should be {aspect_width}:{aspect_height}')
            errors.append(ValidationError(
                msg.format(aspect_width=aspect_width, aspect_height=aspect_heigth)))

    if errors:
        raise ValidationError(errors)
    return image


def validate_hero_image(image):
    validate_image(image, 1300, 600)


def validate_avatar(image):
    validate_image(image, 200, 200)


def validate_logo(image):
    validate_image(image, 200, 200, aspect_ratio=(1, 1))


def validate_idea_image(image):
    validate_image(image, 800, 200)
