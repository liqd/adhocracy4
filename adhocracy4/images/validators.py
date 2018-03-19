from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_image(image, config):

    min_resolution = config.get('min_resolution')
    aspect_ratio = config.get('aspect_ratio', None)
    aspect_margin = config.get('aspect_margin', 0.1)

    errors = []
    min_width, min_height = min_resolution

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

        if abs(target_ratio - actual_ratio) > aspect_margin:
            msg = _(
                'Image aspect ratio should be {aspect_width}:{aspect_height}'
            )
            errors.append(ValidationError(msg.format(
                aspect_width=aspect_width, aspect_height=aspect_heigth
            )))

    if errors:
        raise ValidationError(errors)
    return image
