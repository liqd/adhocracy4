from django.core import checks
from django.utils.translation import gettext_lazy as _

from . import utils


@checks.register()
def check_moderation_itemables(app_configs, **kwargs):
    errors = []
    for model in utils.get_item_models():
        field_names = {field.name for field in model._meta.get_fields()}
        if "is_reviewed" not in field_names:
            errors.append(
                checks.Error(
                    "Moderatable item model '{}' has no 'is_reviewed' field.".format(
                        model._meta.label
                    ),
                    hint=_(
                        "Add an 'is_reviewed' boolean field or remove the model "
                        "from A4_MODERATION_ITEMABLES."
                    ),
                    id="a4moderation.E001",
                )
            )
    return errors
