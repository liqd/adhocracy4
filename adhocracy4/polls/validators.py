import base64
import binascii
import uuid
from io import BytesIO

from django.conf import settings
from django.core import exceptions as django_exceptions
from django.core.files.base import ContentFile
from django.utils.translation import gettext as _
from PIL import Image
from PIL import UnidentifiedImageError
from rest_framework import exceptions as rest_exceptions

from adhocracy4.images.validators import MIN_RESOLUTION_TOLERANCE

MIN_IMAGE_WIDTH = 1500
MIN_IMAGE_HEIGHT = 500


def _get_min_resolution():
    """Return the configured minimum resolution for poll question images.

    Falls back to the historic defaults when the project does not configure
    the ``questionimage`` alias.
    """
    config = getattr(settings, "IMAGE_ALIASES", {}).get("questionimage", {})
    return config.get("min_resolution", (MIN_IMAGE_WIDTH, MIN_IMAGE_HEIGHT))


def validate_poll_question_image(base64_str):
    """Validate a base64-encoded poll question image meets minimum dimensions.

    Returns a ContentFile decoded from the base64 data.
    Returns None if the input is empty/null.
    Raises rest_framework.exceptions.ValidationError if dimensions are too small.
    """
    if not base64_str or base64_str == "":
        return None

    if "base64," not in base64_str:
        return None

    try:
        format, imgstr = base64_str.split(";base64,")
        ext = format.split("/")[-1]
        image_data = base64.b64decode(imgstr)
        img = Image.open(BytesIO(image_data))
    except (binascii.Error, UnidentifiedImageError, OSError, ValueError):
        raise rest_exceptions.ValidationError(
            {"image_base64": [_("The uploaded file is not a valid image.")]}
        )

    min_width, min_height = _get_min_resolution()
    check_width = max(0, min_width - MIN_RESOLUTION_TOLERANCE)
    check_height = max(0, min_height - MIN_RESOLUTION_TOLERANCE)

    errors = {}
    if img.width < check_width:
        errors["image_base64"] = [
            _("Image must be at least %(width)s pixels wide.") % {"width": min_width}
        ]
    if img.height < check_height:
        errors["image_base64"] = [
            _("Image must be at least %(height)s pixels high.") % {"height": min_height}
        ]
    if errors:
        raise rest_exceptions.ValidationError(errors)

    return ContentFile(image_data, name=f"{uuid.uuid4()}.{ext}")


def single_item_per_module(module, model, pk=None):
    siblings = model.objects.filter(module=module)

    if pk:
        siblings = siblings.exclude(pk=pk)

    if len(siblings) > 0:
        raise django_exceptions.ValidationError(
            {
                django_exceptions.NON_FIELD_ERRORS: [
                    _("Item of type %(item)s for that module already exists")
                    % {"item": model.__name__}
                ]
            }
        )


def question_belongs_to_poll(question, poll_pk):
    if question.poll.pk != poll_pk:
        raise rest_exceptions.ValidationError(
            {
                "question": [
                    _("Question has to belong to the poll set in the url."),
                ]
            }
        )


def choice_belongs_to_question(choice, question_pk):
    if question_pk != choice.question.pk:
        raise rest_exceptions.ValidationError(
            {
                "choice": [
                    _("Choice has to belong to the question set in the url."),
                ]
            }
        )


def single_vote_per_user(user, content_id, choice, pk=None):
    from .models import Vote  # avoid circular import

    qs = Vote.objects.filter(choice=choice)

    if content_id:
        qs = qs.filter(content_id=content_id)
    if user:
        qs = qs.filter(creator=user)

    if pk:
        qs = qs.exclude(pk=pk)

    if qs.exists():
        raise django_exceptions.ValidationError(
            {
                "choice": [
                    _("Only one vote per choice is allowed per user."),
                ]
            }
        )
